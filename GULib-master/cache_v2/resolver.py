"""Read-only exact-match explanation for Cache V2.1.

V2.1 deliberately does not compute Artifacts, write payloads, or execute the
compatible/prefix lookup planned for V2.2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple, Union

from .contracts import (
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    VerificationStatus,
)
from .index import CacheIndex


@dataclass(frozen=True)
class ResolveExplanation:
    artifact_type: ArtifactType
    recipe_hash: str
    exact_candidate: Optional[Dict[str, Any]]
    status: Optional[ArtifactStatus]
    verification_status: Optional[VerificationStatus]
    conflicts: Tuple[Dict[str, Any], ...]
    legacy_exact_candidates: Tuple[Dict[str, Any], ...]
    dependency_issues: Tuple[Dict[str, Any], ...]
    hit: bool
    miss_reasons: Tuple[str, ...]
    lookup_policy: str = "exact_only"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_type": self.artifact_type.value,
            "recipe_hash": self.recipe_hash,
            "lookup_policy": self.lookup_policy,
            "exact_candidate": self.exact_candidate,
            "status": None if self.status is None else self.status.value,
            "verification_status": None
            if self.verification_status is None
            else self.verification_status.value,
            "conflicts": list(self.conflicts),
            "conflict_count": len(self.conflicts),
            "legacy_exact_candidates": list(self.legacy_exact_candidates),
            "legacy_exact_candidate_count": len(self.legacy_exact_candidates),
            "dependency_issues": list(self.dependency_issues),
            "hit": self.hit,
            "miss_reasons": list(self.miss_reasons),
        }


class ArtifactResolver:
    """Explain exact CacheIndex candidates without executing computation."""

    def __init__(self, index: CacheIndex):
        if not isinstance(index, CacheIndex):
            raise TypeError("ArtifactResolver requires CacheIndex")
        self.index = index

    def explain_exact(
        self,
        artifact_type: Union[ArtifactType, str],
        recipe: Union[ArtifactRecipe, Mapping[str, Any]],
    ) -> ResolveExplanation:
        type_value = ArtifactType(artifact_type)
        recipe_value = (
            recipe if isinstance(recipe, ArtifactRecipe) else ArtifactRecipe(recipe)
        )
        candidate = self.index.find_artifact(type_value, recipe_value.recipe_hash)
        conflicts: List[Dict[str, Any]] = self.index.conflicts(
            artifact_type=type_value, recipe_hash=recipe_value.recipe_hash
        )
        legacy_candidates: List[Dict[str, Any]] = self.index.legacy_sources(
            artifact_type=type_value, recipe_hash=recipe_value.recipe_hash
        )

        status: Optional[ArtifactStatus] = None
        verification: Optional[VerificationStatus] = None
        miss_reasons: List[str] = []
        dependency_issues: List[Dict[str, Any]] = []
        hit = False
        if candidate is None:
            miss_reasons.append("no_exact_candidate")
            if legacy_candidates:
                miss_reasons.append("legacy_exact_candidate_not_authoritative")
                verification_values = sorted(
                    {
                        str(item.get("verification_status", "unknown"))
                        for item in legacy_candidates
                    }
                )
                for value in verification_values:
                    miss_reasons.append(
                        "legacy_candidate_verification_{0}".format(value)
                    )
        else:
            try:
                status = ArtifactStatus(candidate["status"])
            except (KeyError, TypeError, ValueError):
                miss_reasons.append("candidate_has_invalid_status")
            try:
                verification = VerificationStatus(candidate["verification_status"])
            except (KeyError, TypeError, ValueError):
                miss_reasons.append("candidate_has_invalid_verification_status")

            if status is not None and status != ArtifactStatus.VALID:
                miss_reasons.append("candidate_status_{0}".format(status.value))
            if (
                verification is not None
                and verification != VerificationStatus.VERIFIED
            ):
                miss_reasons.append(
                    "candidate_verification_{0}".format(verification.value)
                )
            hit = (
                status == ArtifactStatus.VALID
                and verification == VerificationStatus.VERIFIED
                and not miss_reasons
            )

        # A conflicting content observation never becomes a second formal
        # Artifact, but its existence makes the Recipe unsafe to resolve
        # automatically. Keep the original row unchanged and fail closed.
        if conflicts:
            miss_reasons.append("recipe_conflict_present")
            hit = False

        if candidate is not None:
            dependency_issues = self._dependency_issues(candidate["artifact_id"])
            for issue in dependency_issues:
                for reason in issue["reasons"]:
                    miss_reasons.append(
                        "dependency_{0}_{1}".format(issue["artifact_id"], reason)
                    )
            if dependency_issues:
                hit = False

        return ResolveExplanation(
            artifact_type=type_value,
            recipe_hash=recipe_value.recipe_hash,
            exact_candidate=candidate,
            status=status,
            verification_status=verification,
            conflicts=tuple(conflicts),
            legacy_exact_candidates=tuple(legacy_candidates),
            dependency_issues=tuple(dependency_issues),
            hit=hit,
            miss_reasons=tuple(miss_reasons),
        )

    def _dependency_issues(self, artifact_id: str) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        visited: Set[str] = set()

        def visit(child_id: str, path: Tuple[str, ...]) -> None:
            for parent_id in self.index.parents(child_id):
                if parent_id in path:
                    issues.append(
                        {
                            "artifact_id": parent_id,
                            "path": list(path + (parent_id,)),
                            "reasons": ["cycle_detected"],
                        }
                    )
                    continue
                if parent_id in visited:
                    continue
                visited.add(parent_id)
                parent = self.index.get_artifact(parent_id)
                reasons: List[str] = []
                parent_status = ArtifactStatus(parent["status"])
                parent_verification = VerificationStatus(
                    parent["verification_status"]
                )
                if parent_status != ArtifactStatus.VALID:
                    reasons.append("status_{0}".format(parent_status.value))
                if parent_verification != VerificationStatus.VERIFIED:
                    reasons.append(
                        "verification_{0}".format(parent_verification.value)
                    )
                parent_conflicts = self.index.conflicts(
                    artifact_type=parent["artifact_type"],
                    recipe_hash=parent["recipe_hash"],
                )
                if parent_conflicts:
                    reasons.append("conflict_present")
                if reasons:
                    issues.append(
                        {
                            "artifact_id": parent_id,
                            "path": list(path + (parent_id,)),
                            "reasons": reasons,
                        }
                    )
                visit(parent_id, path + (parent_id,))

        visit(artifact_id, (artifact_id,))
        return issues

    def explain(
        self,
        artifact_type: Union[ArtifactType, str],
        recipe: Union[ArtifactRecipe, Mapping[str, Any]],
    ) -> ResolveExplanation:
        return self.explain_exact(artifact_type, recipe)


def explain_exact(
    index: CacheIndex,
    artifact_type: Union[ArtifactType, str],
    recipe: Union[ArtifactRecipe, Mapping[str, Any]],
) -> ResolveExplanation:
    """Convenience wrapper for one exact-only explanation."""

    return ArtifactResolver(index).explain_exact(artifact_type, recipe)
