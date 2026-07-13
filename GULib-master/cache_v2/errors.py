"""Exception hierarchy for the Cache V2 machine contract.

This module is intentionally dependency-free and has no import-time side
effects.  Index and CLI layers may translate these exceptions into their own
exit codes, but must not turn them into cache misses.
"""


class CacheV2Error(Exception):
    """Base class for all explicit Cache V2 failures."""


class ContractValidationError(CacheV2Error, ValueError):
    """A machine-contract value is malformed or internally inconsistent."""


class CanonicalizationError(ContractValidationError):
    """A value cannot be represented by the canonical Recipe encoding."""


class ForbiddenRecipeFieldError(ContractValidationError):
    """A Recipe contains experiment/config/report ownership fields."""

    def __init__(self, field_paths):
        self.field_paths = tuple(field_paths)
        message = "forbidden non-Artifact Recipe field(s): {0}".format(
            ", ".join(self.field_paths)
        )
        super().__init__(message)


class PathValidationError(ContractValidationError):
    """A path is ambiguous, traversing, or has the wrong path kind."""


class HashValidationError(ContractValidationError):
    """A required SHA-256 digest is not 64 lowercase hexadecimal chars."""


class CacheIndexError(CacheV2Error):
    """A CacheIndex operation failed and must fail closed."""


class SchemaVersionError(CacheIndexError):
    """The database schema version is missing, inconsistent, or unsupported."""


class IndexNotFoundError(CacheIndexError):
    """A read-only operation was requested for a missing CacheIndex."""


class ArtifactNotFoundError(CacheIndexError):
    """An Artifact referenced by an index operation does not exist."""


class DependencyCycleError(CacheIndexError):
    """A dependency edge would introduce a cycle in the Artifact DAG."""


class LegacySourceChangedError(CacheV2Error):
    """Legacy sources changed between the read-only scan and index apply."""
