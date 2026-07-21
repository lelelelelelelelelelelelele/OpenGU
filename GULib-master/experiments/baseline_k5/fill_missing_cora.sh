#!/usr/bin/env bash
set -euo pipefail

# Compatibility wrapper.  The Python entrypoint owns the v2 schema, canonical
# output root, resume validation, aggregation, and failure status.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"
exec "$PYTHON" "$SCRIPT_DIR/fill_missing_cora.py" "$@"
