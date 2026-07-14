import sys

# The default ``legacy index`` command is a true zero-write dry-run, including
# on a fresh checkout where importing Python modules would otherwise create
# ``__pycache__`` files.
sys.dont_write_bytecode = True

import argparse
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cache_v2 import (  # noqa: E402
    ArtifactNotFoundError,
    ArtifactRecipe,
    ArtifactType,
    CacheV2Error,
    IndexNotFoundError,
)
from cache_v2.legacy import LegacyIndexer  # noqa: E402


DEFAULT_DB = REPO_ROOT / "results" / "cache_v2" / "index.sqlite"
DEFAULT_STORE_ROOT = REPO_ROOT / "results" / "cache_v2"
DEFAULT_DATASET_ROOT = REPO_ROOT / "data" / "raw"
DEFAULT_LEGACY_RESULTS_ROOT = REPO_ROOT / "results"


def _json_ready(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_ready(item) for item in value]
    keys = getattr(value, "keys", None)
    if callable(keys):
        try:
            return {str(key): _json_ready(value[key]) for key in keys()}
        except (KeyError, TypeError, AttributeError):
            pass
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return _json_ready(to_dict())
    if hasattr(value, "__dict__"):
        return _json_ready(vars(value))
    return str(value)


def _emit(payload: Any, stream: Any = None) -> None:
    target = stream or sys.stdout
    print(
        json.dumps(
            _json_ready(payload),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        ),
        file=target,
    )


def _error(code: str, message: str, **details: Any) -> int:
    _emit(
        {"ok": False, "error": {"code": code, "message": message, "details": details}},
        stream=sys.stderr,
    )
    return 2


def _resolve_repo_path(value: Any) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def _load_index_class() -> Any:
    from cache_v2.index import CacheIndex

    return CacheIndex


def _open_existing_index(db_value: Any) -> Any:
    db_path = _resolve_repo_path(db_value)
    if not db_path.is_file():
        raise IndexNotFoundError("Cache V2 index not found: {0}".format(db_path))
    index = _load_index_class()(db_path)
    for method_name in (
        "check_schema",
        "check_schema_version",
        "validate_schema",
        "check_version",
    ):
        method = getattr(index, method_name, None)
        if callable(method):
            method()
            break
    return index


def _cmd_legacy_index(args: argparse.Namespace) -> int:
    if args.apply and args.dry_run:
        return _error(
            "invalid_arguments", "--apply and --dry-run are mutually exclusive"
        )
    root = _resolve_repo_path(args.root)
    indexer = LegacyIndexer(root, sample_limit=args.samples)
    report = indexer.scan()
    payload: Dict[str, Any] = {
        "ok": True,
        "mode": "apply" if args.apply else "dry-run",
        "report": report.to_dict(
            include_records=bool(args.include_records), sample_limit=args.samples
        ),
    }
    if not args.apply:
        payload["writes"] = []
        payload["index_path"] = str(indexer.index_path)
        _emit(payload)
        return 0

    CacheIndex = _load_index_class()
    index = CacheIndex(indexer.index_path)
    indexer.verify_report_sources(report)
    initialize = getattr(index, "initialize", None)
    if not callable(initialize):
        return _error("index_api_error", "CacheIndex lacks initialize()")
    initialize()
    payload["apply"] = indexer.apply(index, report)
    _emit(payload)
    return 0


def _cmd_artifact_status(args: argparse.Namespace) -> int:
    index = _open_existing_index(args.db)
    status = index.get_status(args.artifact_id)
    get_artifact = getattr(index, "get_artifact", None)
    artifact = get_artifact(args.artifact_id) if callable(get_artifact) else None
    conflicts_method = getattr(index, "conflicts", None)
    conflicts = (
        conflicts_method(
            artifact_type=artifact.get("artifact_type"),
            recipe_hash=artifact.get("recipe_hash"),
        )
        if callable(conflicts_method)
        else []
    )
    _emit(
        {
            "ok": True,
            "artifact_id": args.artifact_id,
            "status": status,
            "artifact": artifact,
            "conflicts": conflicts,
        }
    )
    return 0


def _cmd_artifact_relation(args: argparse.Namespace, relation: str) -> int:
    index = _open_existing_index(args.db)
    method = getattr(index, relation)
    values = method(args.artifact_id)
    _emit(
        {
            "ok": True,
            "artifact_id": args.artifact_id,
            "relation": relation,
            relation: values,
        }
    )
    return 0


def _load_recipe(path_value: Any) -> ArtifactRecipe:
    path = _resolve_repo_path(path_value)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(
            "recipe JSON could not be read: {0}: {1}".format(path, exc)
        )
    if not isinstance(payload, dict):
        raise ValueError("recipe JSON root must be an object")
    # ArtifactRecipe.to_dict() has one exact wrapper shape.  A plain Recipe is
    # allowed to use a semantic field literally named ``fields``; never drop
    # its sibling identity fields by guessing that it is a wrapper.
    if set(payload) == {"recipe_version", "fields"}:
        fields = payload["fields"]
        recipe_version = payload["recipe_version"]
        if not isinstance(fields, dict):
            raise ValueError("recipe.fields must be an object")
        return ArtifactRecipe(fields=fields, recipe_version=recipe_version)
    return ArtifactRecipe(fields=payload)


def _status_text(candidate: Any) -> Optional[str]:
    if candidate is None:
        return None
    if isinstance(candidate, dict):
        value = candidate.get("status")
    else:
        value = getattr(candidate, "status", None)
    if isinstance(value, Enum):
        return value.value
    return str(value) if value is not None else None


def _cmd_resolve_explain(args: argparse.Namespace) -> int:
    index = _open_existing_index(args.db)
    artifact_type = ArtifactType(args.artifact_type)
    recipe = _load_recipe(args.recipe)
    try:
        from cache_v2.resolver import ArtifactResolver

        resolution = ArtifactResolver(index).explain_exact(artifact_type, recipe)
    except ImportError:
        resolution = None
    if resolution is not None:
        explanation = resolution.to_dict()
        if explanation.get("conflicts"):
            explanation["hit"] = False
            miss_reasons = list(explanation.get("miss_reasons") or [])
            if not any("conflict" in str(reason) for reason in miss_reasons):
                miss_reasons.append("recipe_has_conflict")
            explanation["miss_reasons"] = miss_reasons
        _emit(
            {
                "ok": True,
                "lookup": "exact-only",
                "artifact_type": artifact_type,
                "recipe_hash": recipe.recipe_hash,
                "recipe": recipe,
                "explanation": explanation,
                "execution_performed": False,
                "writes": [],
            }
        )
        return 0
    explain_method = getattr(index, "explain_exact", None)
    if callable(explain_method):
        explanation = explain_method(artifact_type, recipe.recipe_hash)
        _emit(
            {
                "ok": True,
                "lookup": "exact-only",
                "artifact_type": artifact_type,
                "recipe_hash": recipe.recipe_hash,
                "recipe": recipe,
                "explanation": explanation,
                "execution_performed": False,
                "writes": [],
            }
        )
        return 0

    candidate = index.find_artifact(artifact_type, recipe.recipe_hash)
    conflicts_method = getattr(index, "conflicts", None)
    conflicts = (
        conflicts_method(artifact_type=artifact_type, recipe_hash=recipe.recipe_hash)
        if callable(conflicts_method)
        else []
    )
    status = _status_text(candidate)
    reasons = []
    if candidate is None:
        reasons.append("no_exact_candidate")
    elif status != "valid":
        reasons.append("candidate_status_{0}".format(status or "unknown"))
    if conflicts:
        reasons.append("recipe_has_conflict")
    hit = candidate is not None and status == "valid" and not conflicts
    _emit(
        {
            "ok": True,
            "lookup": "exact-only",
            "artifact_type": artifact_type,
            "recipe_hash": recipe.recipe_hash,
            "recipe": recipe,
            "exact_candidate": candidate,
            "candidate_status": status,
            "conflicts": conflicts,
            "hit": hit,
            "miss_reasons": [] if hit else reasons,
            "execution_performed": False,
            "writes": [],
        }
    )
    return 0


def _selection_paths(args: argparse.Namespace) -> Dict[str, Path]:
    return {
        "config_path": _resolve_repo_path(args.config),
        "dataset_root": _resolve_repo_path(args.dataset_root),
        "store_root": _resolve_repo_path(args.store_root),
        "legacy_results_root": _resolve_repo_path(args.legacy_results_root),
    }


def _cmd_selection_plan(args: argparse.Namespace) -> int:
    from cache_v2.selection_materializer import plan_selection

    paths = _selection_paths(args)
    document = plan_selection(
        paths["config_path"],
        paths["dataset_root"],
        paths["store_root"],
        paths["legacy_results_root"],
        allow_download=bool(args.allow_download),
        split_seed=args.split_seed,
    )
    _emit(document)
    return 0


def _cmd_selection_materialize(args: argparse.Namespace) -> int:
    if not args.apply:
        return _error(
            "apply_required",
            "selection materialize is write-capable; pass --apply explicitly",
        )
    from cache_v2.selection_materializer import materialize_selection

    paths = _selection_paths(args)
    document = materialize_selection(
        paths["config_path"],
        paths["dataset_root"],
        paths["store_root"],
        paths["legacy_results_root"],
        allow_download=bool(args.allow_download),
        split_seed=args.split_seed,
        verify=bool(args.verify),
        fail_if_producer_called=bool(args.fail_if_producer_called),
        compare_legacy=bool(args.compare_legacy),
        include_nodes=bool(args.include_nodes),
    )
    _emit(document)
    return 0


def _add_selection_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", required=True, help="experiment YAML request envelope")
    parser.add_argument(
        "--dataset-root",
        default=str(DEFAULT_DATASET_ROOT),
        help="repo-anchored or absolute PyG/OGB dataset root",
    )
    parser.add_argument(
        "--store-root",
        default=str(DEFAULT_STORE_ROOT),
        help="repo-anchored or absolute V2 ArtifactStore root",
    )
    parser.add_argument(
        "--legacy-results-root",
        default=str(DEFAULT_LEGACY_RESULTS_ROOT),
        help="read-only Legacy results root used for invariants/comparison",
    )
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="explicitly allow the dataset adapter to download/process missing data",
    )
    parser.add_argument(
        "--split-seed",
        type=int,
        help="override the default OpenGU split seed (first YAML seed)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python scripts/cachectl.py",
        description="Cache V2 exact index, inspection, and opt-in Selection materialization CLI",
    )
    top = parser.add_subparsers(dest="command", required=True)

    legacy = top.add_parser("legacy", help="inspect read-only legacy sources")
    legacy_sub = legacy.add_subparsers(dest="legacy_command", required=True)
    legacy_index = legacy_sub.add_parser("index", help="scan or explicitly index legacy sources")
    legacy_index.add_argument("--root", default="results")
    legacy_index.add_argument(
        "--dry-run",
        action="store_true",
        help="explicitly select the default zero-write mode",
    )
    legacy_index.add_argument(
        "--apply",
        action="store_true",
        help="write only <root>/cache_v2/index.sqlite",
    )
    legacy_index.add_argument("--samples", type=int, default=5)
    legacy_index.add_argument(
        "--include-records",
        action="store_true",
        help="include the complete in-memory plan in JSON output",
    )
    legacy_index.set_defaults(handler=_cmd_legacy_index)

    artifact = top.add_parser("artifact", help="query indexed Artifact metadata")
    artifact_sub = artifact.add_subparsers(dest="artifact_command", required=True)
    for name, help_text in (
        ("status", "show Artifact status and exact conflicts"),
        ("parents", "show direct parent Artifacts"),
        ("children", "show direct child Artifacts"),
        ("consumers", "show direct consumers"),
    ):
        sub = artifact_sub.add_parser(name, help=help_text)
        sub.add_argument("artifact_id")
        sub.add_argument("--db", default=str(DEFAULT_DB))
        if name == "status":
            sub.set_defaults(handler=_cmd_artifact_status)
        else:
            sub.set_defaults(
                handler=(lambda relation: lambda args: _cmd_artifact_relation(args, relation))(
                    name
                )
            )

    resolve = top.add_parser("resolve", help="explain exact Cache resolution")
    resolve_sub = resolve.add_subparsers(dest="resolve_command", required=True)
    explain = resolve_sub.add_parser(
        "explain", help="explain exact candidate, status, conflict, or miss"
    )
    explain.add_argument(
        "--type",
        dest="artifact_type",
        choices=[item.value for item in ArtifactType],
        required=True,
    )
    explain.add_argument("--recipe", required=True)
    explain.add_argument("--db", default=str(DEFAULT_DB))
    explain.set_defaults(handler=_cmd_resolve_explain)

    selection = top.add_parser(
        "selection", help="plan or explicitly materialize exact Selection Artifacts"
    )
    selection_sub = selection.add_subparsers(
        dest="selection_command", required=True
    )
    selection_plan = selection_sub.add_parser(
        "plan", help="compile YAML to unique exact Recipes without store writes"
    )
    _add_selection_common_arguments(selection_plan)
    selection_plan.set_defaults(handler=_cmd_selection_plan)

    selection_materialize = selection_sub.add_parser(
        "materialize", help="compute misses and write only to the V2 ArtifactStore"
    )
    _add_selection_common_arguments(selection_materialize)
    selection_materialize.add_argument(
        "--apply",
        action="store_true",
        help="required acknowledgement for V2 store writes",
    )
    selection_materialize.add_argument(
        "--verify",
        action="store_true",
        help="perform an independent warm exact hit with a fail-if-called producer sentinel",
    )
    selection_materialize.add_argument(
        "--fail-if-producer-called",
        action="store_true",
        help="warm-only mode: fail closed instead of computing an exact miss",
    )
    selection_materialize.add_argument(
        "--compare-legacy",
        action="store_true",
        help="compare same-seed Legacy nodes read-only; never use them for resolution",
    )
    selection_materialize.add_argument(
        "--include-nodes",
        action="store_true",
        help="include ordered selected nodes in JSON output",
    )
    selection_materialize.set_defaults(handler=_cmd_selection_materialize)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except ArtifactNotFoundError as exc:
        _emit(
            {"ok": False, "error": {"code": "artifact_not_found", "message": str(exc)}},
            stream=sys.stderr,
        )
        return 1
    except (IndexNotFoundError, CacheV2Error, TypeError, ValueError, OSError) as exc:
        return _error(type(exc).__name__, str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
