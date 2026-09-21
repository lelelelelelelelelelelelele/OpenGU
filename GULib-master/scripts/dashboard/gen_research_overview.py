"""Build the independent Work Plan. No Block or execution writes."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.dashboard.workplan_view import main

if __name__ == '__main__':
    raise SystemExit(main())
