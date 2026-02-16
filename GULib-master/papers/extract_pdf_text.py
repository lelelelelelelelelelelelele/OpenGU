#!/usr/bin/env python3
"""
Extract searchable UTF-8 text from PDFs in papers/papers.csv.

Why:
- The synthesis must not hallucinate; we ground every method/eval detail in local PDFs.
- We avoid modifying the global Python environment by using papers/_vendor for deps.

Outputs:
- papers/raw/text/<arxiv_id>.txt
- papers/raw/text_index.json (stats + errors)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
TEXT_DIR = os.path.join(RAW_DIR, "text")


def _ensure_dirs() -> None:
    os.makedirs(TEXT_DIR, exist_ok=True)


def _import_pypdf():
    vendor = os.path.join(BASE_DIR, "_vendor")
    if os.path.isdir(vendor):
        sys.path.insert(0, vendor)
    from pypdf import PdfReader  # type: ignore

    return PdfReader


@dataclass
class ExtractStats:
    arxiv_id: str
    pdf_path: str
    txt_path: str
    pages: int
    chars: int
    ok: bool
    error: str


def _read_papers_csv(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _extract_one(PdfReader, arxiv_id: str, pdf_path: str, txt_path: str) -> ExtractStats:
    try:
        reader = PdfReader(pdf_path)
        pages = len(reader.pages)
        parts: List[str] = []
        for i in range(pages):
            text = reader.pages[i].extract_text() or ""
            parts.append(text)
        full = "\n\n".join(parts).replace("\x00", "").strip()
        with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(full)
        return ExtractStats(
            arxiv_id=arxiv_id,
            pdf_path=pdf_path,
            txt_path=txt_path,
            pages=pages,
            chars=len(full),
            ok=True,
            error="",
        )
    except Exception as exc:  # noqa: BLE001
        return ExtractStats(
            arxiv_id=arxiv_id,
            pdf_path=pdf_path,
            txt_path=txt_path,
            pages=0,
            chars=0,
            ok=False,
            error=str(exc),
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(BASE_DIR, "papers.csv"))
    ap.add_argument("--force", action="store_true", help="re-extract even if txt exists")
    args = ap.parse_args()

    _ensure_dirs()
    PdfReader = _import_pypdf()

    rows = _read_papers_csv(args.csv)
    stats: List[ExtractStats] = []

    for r in rows:
        arxiv_id = (r.get("arxiv_id") or "").strip()
        local_path = (r.get("local_path") or "").strip()
        if not arxiv_id:
            continue
        if not local_path or local_path == "unknown":
            stats.append(
                ExtractStats(
                    arxiv_id=arxiv_id,
                    pdf_path=local_path or "unknown",
                    txt_path="",
                    pages=0,
                    chars=0,
                    ok=False,
                    error="missing local_path in papers.csv",
                )
            )
            continue

        pdf_path = os.path.normpath(os.path.join(os.path.dirname(BASE_DIR), local_path))
        txt_path = os.path.join(TEXT_DIR, f"{arxiv_id}.txt")
        if (not args.force) and os.path.exists(txt_path):
            try:
                size = os.path.getsize(txt_path)
            except OSError:
                size = 0
            stats.append(
                ExtractStats(
                    arxiv_id=arxiv_id,
                    pdf_path=pdf_path,
                    txt_path=txt_path,
                    pages=-1,
                    chars=size,
                    ok=True,
                    error="skipped (exists)",
                )
            )
            continue

        stats.append(_extract_one(PdfReader, arxiv_id, pdf_path, txt_path))

    index = [asdict(s) for s in stats]
    with open(os.path.join(RAW_DIR, "text_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    ok = sum(1 for s in stats if s.ok)
    fail = len(stats) - ok
    print(f"extracted ok={ok} fail={fail} -> {TEXT_DIR}")


if __name__ == "__main__":
    main()
