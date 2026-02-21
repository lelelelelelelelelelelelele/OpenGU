import os
import re
from typing import Dict, Iterable, Optional, Tuple, Union


def _as_dirs(base_dir: Union[str, Iterable[str]]) -> Iterable[str]:
    if isinstance(base_dir, str):
        return [base_dir]
    return list(base_dir)


def _ratio_variants(ratio: Union[str, float]) -> Iterable[str]:
    raw = str(ratio).strip()
    variants = {raw}
    try:
        numeric = float(raw)
        variants.add(f"{numeric:g}")
        if numeric == 0.1:
            variants.add("0.1")
    except ValueError:
        pass
    return variants


def _candidate_names(dataset: str, method: str, model: str, ratio: Union[str, float]) -> Iterable[str]:
    names = []
    for ratio_text in _ratio_variants(ratio):
        names.append(f"{method}_{model}_{dataset}_r{ratio_text}.log")
    try:
        if float(str(ratio)) == 0.1:
            names.append(f"{method}_{model}_{dataset}.log")
    except ValueError:
        pass
    return names


def _ratio_from_filename(filename: str) -> Optional[float]:
    match = re.search(r"_r([0-9.]+)\.log$", filename)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def resolve_log_path(dataset: str, method: str, model: str, ratio: Union[str, float], base_dir: Union[str, Iterable[str]]) -> Optional[str]:
    target_ratio = None
    try:
        target_ratio = float(str(ratio))
    except ValueError:
        pass

    for directory in _as_dirs(base_dir):
        if not directory or not os.path.isdir(directory):
            continue
        for name in _candidate_names(dataset, method, model, ratio):
            candidate = os.path.join(directory, name)
            if os.path.isfile(candidate):
                return candidate

        prefix = f"{method}_{model}_{dataset}_r"
        for name in os.listdir(directory):
            if not (name.startswith(prefix) and name.endswith(".log")):
                continue
            if target_ratio is None:
                continue
            ratio_in_name = _ratio_from_filename(name)
            if ratio_in_name is None:
                continue
            if abs(ratio_in_name - target_ratio) < 1e-12:
                return os.path.join(directory, name)
    return None


def _extract_f1_after(content: str) -> Optional[float]:
    patterns = [
        r"Unlearn F1 Score:\s*([0-9]*\.?[0-9]+)",
        r"Direct F1 Score:\s*([0-9]*\.?[0-9]+)",
        r"Final Test F1:\s*([0-9]*\.?[0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    return None


def _extract_error(content: str, has_traceback: bool) -> Tuple[Optional[str], Optional[str]]:
    error_msg = None
    error_type = None

    if has_traceback:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        for line in reversed(lines):
            if re.search(r"(Error|Exception):", line):
                error_msg = line
                break
        if error_msg is None:
            error_msg = "Traceback detected"

        lowered = error_msg.lower()
        if "inconsistent numbers of samples" in lowered:
            error_type = "MIA_LENGTH_MISMATCH"
        elif "out of memory" in lowered:
            error_type = "CUDA_OOM"
        else:
            match = re.match(r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)):", error_msg)
            error_type = match.group(1) if match else "TRACEBACK_ERROR"
        return error_type, error_msg

    match = re.search(r"(ValueError|RuntimeError|AssertionError|TypeError|KeyError):\s*(.+)", content)
    if match:
        return match.group(1), f"{match.group(1)}: {match.group(2).strip()}"
    return None, None


def parse_log_quality(log_path: Optional[str]) -> Dict[str, object]:
    result: Dict[str, object] = {
        "ok": False,
        "f1_after": None,
        "has_completion_marker": False,
        "has_traceback": False,
        "error_type": None,
        "error_msg": None,
    }
    if not log_path or not os.path.isfile(log_path):
        return result

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as file_obj:
            content = file_obj.read()
    except OSError as exc:
        result["error_type"] = "LOG_READ_ERROR"
        result["error_msg"] = str(exc)
        return result

    f1_after = _extract_f1_after(content)
    has_traceback = "Traceback" in content
    has_completion_marker = bool(re.search(r"(Performance Metrics|Unlearn F1 Score)", content))
    error_type, error_msg = _extract_error(content, has_traceback)

    result["f1_after"] = f1_after
    result["has_traceback"] = has_traceback
    result["has_completion_marker"] = has_completion_marker
    result["error_type"] = error_type
    result["error_msg"] = error_msg
    result["ok"] = bool(f1_after is not None and has_completion_marker and not has_traceback)
    return result


def should_skip(dataset: str, method: str, model: str, ratio: Union[str, float], base_dir: Union[str, Iterable[str]]) -> Tuple[bool, Dict[str, object], Optional[str]]:
    log_path = resolve_log_path(dataset=dataset, method=method, model=model, ratio=ratio, base_dir=base_dir)
    quality = parse_log_quality(log_path)
    return bool(quality["ok"]), quality, log_path
