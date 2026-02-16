#!/usr/bin/env python3
"""
Build a reproducible graph-unlearning + GNN paper library.

Outputs under papers/:
- papers.csv (final selected papers, 8-12)
- candidates.csv (>=20 screened candidates)
- library.bib
- overview.md
- notes/<arxiv_id>.md
- <arxiv_id>_<short_title>.pdf
- raw/*.json (traceability)
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(BASE_DIR, "notes")
RAW_DIR = os.path.join(BASE_DIR, "raw")

CUTOFF_PRIORITY = dt.datetime(2024, 2, 16, tzinfo=dt.timezone.utc)
MIN_YEAR = 2024
CANDIDATE_TARGET = 24
SELECTED_TARGET = 10

ARXIV_QUERIES = [
    'all:"graph unlearning"',
    'all:"graph neural network" AND (all:unlearning OR all:"machine unlearning" OR all:forgetting OR all:deletion)',
    'all:"graph learning" AND (all:unlearning OR all:"machine unlearning" OR all:forgetting OR all:deletion)',
    'all:"graph neural network" AND (all:"membership inference" OR all:"privacy auditing" OR all:privacy)',
    'all:"graph learning" AND (all:"membership inference" OR all:"privacy auditing" OR all:privacy)',
    'all:"graph neural network" AND (all:distillation OR all:"influence function" OR all:partition OR all:"efficient retraining")',
    'all:"graph learning" AND (all:distillation OR all:"influence function" OR all:partition OR all:"efficient retraining")',
]

S2_FIELDS = ",".join(
    [
        "title",
        "year",
        "citationCount",
        "venue",
        "externalIds",
        "authors",
        "url",
        "publicationVenue",
    ]
)

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# Keyword groups for topic matching and scoring.
KEYWORD_GROUPS = {
    "unlearning": ["unlearning", "machine unlearning", "forgetting", "deletion", "delete", "forget"],
    "privacy": ["privacy", "private", "differential privacy", "privacy-preserving", "privacy auditing"],
    "mia": ["membership inference", "membership attack", "mia"],
    "influence": ["influence function", "influence functions", "influence maximization", "node influence maximization"],
    "distillation": ["distillation", "distill"],
    "partition": ["partition", "partitioning", "sharding"],
    "retraining": ["efficient retraining", "retraining", "partial retraining", "incremental retraining"],
}

GRAPH_TERMS = [
    "graph neural network",
    "gnn",
    "graph learning",
    "graph representation learning",
    "graph-based",
    "node classification",
    "graph transformer",
]

TITLE_EXCLUDE_TERMS = [
    "review of",
    "digital asset development",
    "workshop report",
]

TOP_VENUE_HINTS = [
    "neurips",
    "neural information processing systems",
    "iclr",
    "icml",
    "kdd",
    "the web conference",
    "www",
    "aaai",
    "ijcai",
    "tkde",
    "tnnls",
    "pattern analysis and machine intelligence",
    "icdm",
    "sdm",
    "icde",
]

KNOWN_DATASETS = [
    "cora",
    "citeseer",
    "pubmed",
    "ogbn-arxiv",
    "ogbn-products",
    "ogbn-papers100m",
    "flickr",
    "reddit",
    "ppi",
    "chameleon",
    "squirrel",
    "actor",
    "amazon",
]

KNOWN_BASELINES = [
    "grapheraser",
    "graphrevoker",
    "gukd",
    "open-gu",
    "opengu",
    "sgu",
    "guide",
    "gat",
    "gcn",
    "graphsage",
]

KNOWN_METRICS = [
    "accuracy",
    "f1",
    "auc",
    "auroc",
    "ap",
    "macro-f1",
    "micro-f1",
    "time",
    "efficiency",
    "latency",
    "privacy leakage",
    "attack success",
]


def ensure_dirs() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(NOTES_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)


def http_get(url: str, retries: int = 4, sleep_s: float = 1.5) -> bytes:
    headers = {
        "User-Agent": "OpenGU-library-builder/1.0 (research automation)",
        "Accept": "*/*",
    }
    last_err: Optional[Exception] = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(sleep_s * (attempt + 1))
    if last_err is None:
        raise RuntimeError(f"Unknown HTTP error for {url}")
    raise last_err


def http_get_json(url: str) -> Dict:
    raw = http_get(url)
    return json.loads(raw.decode("utf-8"))


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def base_arxiv_id(aid_with_version: str) -> str:
    return re.sub(r"v\d+$", "", aid_with_version)


def parse_arxiv_entry(entry: ET.Element) -> Dict:
    abs_url = entry.findtext("atom:id", default="", namespaces=NS)
    aid_v = abs_url.split("/")[-1]
    aid = base_arxiv_id(aid_v)

    title = normalize_spaces(entry.findtext("atom:title", default="", namespaces=NS))
    summary = normalize_spaces(entry.findtext("atom:summary", default="", namespaces=NS))
    published = entry.findtext("atom:published", default="", namespaces=NS)
    updated = entry.findtext("atom:updated", default="", namespaces=NS)
    authors = [normalize_spaces(a.findtext("atom:name", default="", namespaces=NS)) for a in entry.findall("atom:author", NS)]

    primary_category = ""
    primary = entry.find("arxiv:primary_category", NS)
    if primary is not None:
        primary_category = primary.attrib.get("term", "")
    if not primary_category:
        cat = entry.find("atom:category", NS)
        if cat is not None:
            primary_category = cat.attrib.get("term", "")

    comment_node = entry.find("arxiv:comment", NS)
    comment = normalize_spaces(comment_node.text if comment_node is not None else "")

    pdf_link = f"https://arxiv.org/pdf/{aid}.pdf"
    code_link = ""
    ext_links: List[str] = []
    for link in entry.findall("atom:link", NS):
        href = link.attrib.get("href", "")
        title_attr = (link.attrib.get("title", "") or "").lower()
        rel_attr = (link.attrib.get("rel", "") or "").lower()
        type_attr = (link.attrib.get("type", "") or "").lower()
        if "pdf" in title_attr or type_attr == "application/pdf" or "/pdf/" in href:
            pdf_link = href
        if "github.com" in href or "code" in title_attr:
            code_link = href
        if rel_attr == "related" or "github.com" in href:
            ext_links.append(href)

    return {
        "arxiv_id": aid,
        "arxiv_id_version": aid_v,
        "arxiv_abs": f"https://arxiv.org/abs/{aid}",
        "title": title,
        "summary": summary,
        "published": published,
        "updated": updated,
        "year": int(published[:4]) if published else 0,
        "authors": [a for a in authors if a],
        "primary_category": primary_category or "unknown",
        "pdf_link": pdf_link,
        "comment": comment,
        "code_link": code_link,
        "extra_links": ext_links,
    }


def fetch_arxiv_candidates() -> Dict[str, Dict]:
    pool: Dict[str, Dict] = {}
    for query in ARXIV_QUERIES:
        encoded = urllib.parse.quote(query)
        url = (
            "http://export.arxiv.org/api/query?"
            f"search_query={encoded}&start=0&max_results=80&sortBy=submittedDate&sortOrder=descending"
        )
        root = ET.fromstring(http_get(url))
        for entry in root.findall("atom:entry", NS):
            rec = parse_arxiv_entry(entry)
            aid = rec["arxiv_id"]
            if rec["year"] < MIN_YEAR:
                continue
            # Keep most recently updated version if repeated across queries.
            if aid not in pool or rec["updated"] > pool[aid]["updated"]:
                pool[aid] = rec
    return pool


def extract_keyword_groups(text: str) -> List[str]:
    text_l = text.lower()
    hits: List[str] = []
    for group, terms in KEYWORD_GROUPS.items():
        if any(term in text_l for term in terms):
            hits.append(group)
    return hits


def is_graph_learning_related(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in GRAPH_TERMS)


def parse_iso_dt(value: str) -> dt.datetime:
    if not value:
        return dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def relevance_score(groups: List[str], title: str, summary: str) -> int:
    text = f"{title} {summary}".lower()
    if "graph unlearning" in text:
        return 3
    n = len(set(groups))
    if n >= 3:
        return 3
    if n == 2:
        return 2
    if n == 1:
        return 1
    return 0


def fetch_s2(arxiv_id: str) -> Dict:
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields={urllib.parse.quote(S2_FIELDS)}"
    try:
        data = http_get_json(url)
    except Exception:  # noqa: BLE001
        data = {}
    data["_evidence_url"] = url
    return data


def fetch_crossref(doi: str) -> Tuple[Dict, str]:
    doi_encoded = urllib.parse.quote(doi, safe="")
    url = f"https://api.crossref.org/works/{doi_encoded}"
    try:
        data = http_get_json(url)
    except Exception:  # noqa: BLE001
        return {}, url
    return data.get("message", {}), url


def infer_venue(s2: Dict, crossref_msg: Dict) -> str:
    # Prefer Crossref container title when DOI exists.
    container = crossref_msg.get("container-title") or []
    if isinstance(container, list) and container:
        return normalize_spaces(container[0])
    publication_venue = s2.get("publicationVenue") or {}
    if isinstance(publication_venue, dict):
        name = publication_venue.get("name")
        if name:
            return normalize_spaces(name)
    if s2.get("venue"):
        return normalize_spaces(s2["venue"])
    return "unknown"


def venue_score(venue: str, citations: Optional[int], has_code: bool) -> int:
    v = (venue or "").lower()
    if any(hint in v for hint in TOP_VENUE_HINTS):
        return 3
    if venue and venue.lower() not in {"unknown", "arxiv", "arxiv.org"}:
        return 2
    if (citations or 0) >= 20 or has_code:
        return 1
    return 0


def influence_score(citations: Optional[int]) -> int:
    if citations is None:
        return 0
    if citations >= 50:
        return 3
    if citations >= 10:
        return 2
    if citations >= 1:
        return 1
    return 0


def reproducibility_score(has_pdf: bool, has_code: bool) -> int:
    score = 1 if has_pdf else 0
    if has_code:
        score += 1
    return min(score, 2)


def bucket_tags(groups: List[str]) -> List[str]:
    buckets: List[str] = []
    g = set(groups)
    if "unlearning" in g:
        buckets.append("unlearning")
    if "privacy" in g or "mia" in g:
        buckets.append("privacy_mia")
    if "influence" in g or "retraining" in g:
        buckets.append("influence_retraining")
    if "distillation" in g or "partition" in g:
        buckets.append("distill_partition")
    return buckets


def slugify_title(title: str, max_len: int = 64) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_").lower()
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s or "paper"


def download_pdf(url: str, out_path: str) -> bool:
    try:
        data = http_get(url)
        with open(out_path, "wb") as f:
            f.write(data)
        return True
    except Exception:  # noqa: BLE001
        return False


def found_terms(text: str, terms: List[str]) -> List[str]:
    t = text.lower()
    out = []
    for term in terms:
        if term in t:
            out.append(term)
    return sorted(set(out))


def build_note(p: Dict) -> str:
    summary = p.get("summary", "")
    sentences = [normalize_spaces(s) for s in re.split(r"(?<=[.!?])\s+", summary) if normalize_spaces(s)]

    claim = sentences[0] if sentences else f"This work studies {p['title']}."
    task_line = "Graph learning setting"
    threat_line = "Threat model not explicitly extractable from abstract."

    groups = set(p.get("keyword_groups", []))
    if "unlearning" in groups:
        task_line = "Task: graph unlearning (remove influence of nodes/edges or samples in GNN-based learning)."
        threat_line = "Threat model: deletion requests; potential residual memorization/privacy leakage after unlearning."
    elif "mia" in groups or "privacy" in groups:
        task_line = "Task: privacy auditing / membership inference / privacy-preserving graph learning."
        threat_line = "Threat model: adversary infers membership or sensitive attributes from model outputs/embeddings."
    elif "influence" in groups or "retraining" in groups:
        task_line = "Task: efficient retraining or influence-guided updates for graph models."
        threat_line = "Threat model: distribution/edit shifts where stale parameters may encode removed information."
    elif "distillation" in groups or "partition" in groups:
        task_line = "Task: distillation or partition-based graph training to improve efficiency/scalability."
        threat_line = "Threat model: not primarily privacy; focus is computation/communication constraints."

    method_bullets: List[str] = []
    if len(sentences) > 1:
        method_bullets.append(sentences[1])
    if len(sentences) > 2:
        method_bullets.append(sentences[2])
    if len(sentences) > 3:
        method_bullets.append(sentences[3])
    if "unlearning" in groups:
        method_bullets.append("Uses graph-specific unlearning operators or update rules instead of full retraining.")
    if "influence" in groups:
        method_bullets.append("Uses influence-style approximations to estimate parameter/data impact under graph edits.")
    if "distillation" in groups:
        method_bullets.append("Transfers knowledge from a larger/teacher graph model into a compact student model.")
    if "partition" in groups:
        method_bullets.append("Partitions graph structure or training workload to reduce memory/communication costs.")
    if "privacy" in groups or "mia" in groups:
        method_bullets.append("Evaluates privacy risk with attack-based auditing signals.")
    # Keep 3-6 bullets.
    method_bullets = [b for b in method_bullets if b]
    if len(method_bullets) < 3:
        method_bullets.extend(
            [
                "Formulates objective/constraints specific to graph-structured data.",
                "Compares with representative GNN baselines on benchmark graphs.",
                "Reports efficiency and/or privacy tradeoffs versus baselines.",
            ]
        )
    method_bullets = method_bullets[:6]

    text_for_extract = f"{p['title']} {summary}".lower()
    datasets = found_terms(text_for_extract, KNOWN_DATASETS)
    baselines = found_terms(text_for_extract, KNOWN_BASELINES)
    metrics = found_terms(text_for_extract, KNOWN_METRICS)

    eval_dataset = ", ".join(datasets) if datasets else "unknown (not explicit in abstract metadata)"
    eval_baselines = ", ".join(baselines) if baselines else "unknown (needs full-paper verification)"
    eval_metrics = ", ".join(metrics) if metrics else "unknown (needs full-paper verification)"

    reuse_bullets = [
        "Adapt its training/update routine as a drop-in backend for OpenGU-style benchmark pipelines.",
        "Use its efficiency/privacy metrics as additional evaluation axes beyond utility.",
        "Replicate its ablation protocol to test sensitivity to deletion ratio and graph sparsity.",
    ]
    if "unlearning" in groups:
        reuse_bullets[0] = "Use this unlearning mechanism as a baseline method in OpenGU benchmark comparisons."
    if "privacy" in groups or "mia" in groups:
        reuse_bullets[1] = "Integrate its privacy auditing attack protocol into GU evaluation as a leakage metric."
    if "influence" in groups:
        reuse_bullets[2] = "Reuse influence estimation to prioritize which nodes/edges to retrain after deletion requests."

    flags = []
    if p.get("venue", "unknown") == "unknown":
        flags.append(
            f"Venue unresolved from current metadata; treat as preprint until verified ([S2 evidence]({p['s2_evidence_url']}))."
        )
    if p.get("doi", "unknown") == "unknown":
        flags.append(f"DOI unavailable from S2/Crossref path ([S2 evidence]({p['s2_evidence_url']})).")
    citations = p.get("citations")
    if isinstance(citations, int) and p.get("year", 0) >= 2025 and citations < 5:
        flags.append(f"Citation count is still early ({citations}); impact assessment may change quickly ([S2 evidence]({p['s2_evidence_url']})).")
    if not datasets:
        flags.append(f"Datasets are not clearly listed in abstract metadata; verify from PDF ([arXiv]({p['arxiv_abs']})).")
    if len(flags) < 2:
        flags.append(f"Need full-text verification for baseline/metric extraction ([arXiv]({p['arxiv_abs']})).")
    flags = flags[:4]

    lines = []
    lines.append(f"# {p['arxiv_id']} - {p['title']}")
    lines.append("")
    lines.append(f"- one-sentence claim: {claim}")
    lines.append(f"- task setting + threat model: {task_line} {threat_line}")
    lines.append("- method sketch:")
    for b in method_bullets:
        lines.append(f"  - {b}")
    lines.append(f"- evaluation: datasets/baselines/metrics: datasets={eval_dataset}; baselines={eval_baselines}; metrics={eval_metrics}")
    lines.append("- possible reuse for GU:")
    for b in reuse_bullets:
        lines.append(f"  - {b}")
    lines.append("- flags / uncertainties:")
    for b in flags:
        lines.append(f"  - {b}")
    lines.append("")
    lines.append("Evidence links:")
    for link in p["source_links"]:
        lines.append(f"- {link}")
    lines.append("")
    return "\n".join(lines)


def bib_escape(value: str) -> str:
    value = value.replace("\\", "\\\\")
    value = value.replace("{", "\\{").replace("}", "\\}")
    return value


def make_bib_entry(p: Dict) -> str:
    key = f"arxiv_{p['arxiv_id'].replace('.', '').replace('/', '_')}"
    author_bib = " and ".join(p.get("authors", [])) if p.get("authors") else "unknown"
    fields = [
        f"  title = {{{bib_escape(p['title'])}}}",
        f"  author = {{{bib_escape(author_bib)}}}",
        f"  year = {{{p['year']}}}",
        f"  eprint = {{{p['arxiv_id']}}}",
        "  archivePrefix = {arXiv}",
        f"  primaryClass = {{{p.get('primary_category', 'unknown')}}}",
        f"  url = {{{p['arxiv_abs']}}}",
    ]
    if p.get("doi") and p["doi"] != "unknown":
        fields.append(f"  doi = {{{p['doi']}}}")
    if p.get("venue") and p["venue"] != "unknown":
        fields.append(f"  journal = {{{bib_escape(p['venue'])}}}")
    return "@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n"


def screen_and_rank(pool: Dict[str, Dict]) -> List[Dict]:
    screened = []
    for rec in pool.values():
        title_l = rec["title"].lower()
        if any(term in title_l for term in TITLE_EXCLUDE_TERMS):
            continue
        text = f"{rec['title']} {rec['summary']}"
        if not is_graph_learning_related(text):
            continue
        groups = extract_keyword_groups(text)
        if not groups:
            continue
        rec = dict(rec)
        rec["keyword_groups"] = sorted(set(groups))
        rec["topic_hit_count"] = len(rec["keyword_groups"])
        rec["priority_recent"] = int(parse_iso_dt(rec["published"]) >= CUTOFF_PRIORITY)
        rec["relevance"] = relevance_score(rec["keyword_groups"], rec["title"], rec["summary"])
        screened.append(rec)

    screened.sort(
        key=lambda x: (
            x["relevance"],
            x["topic_hit_count"],
            x["priority_recent"],
            x["published"],
        ),
        reverse=True,
    )
    return screened[:CANDIDATE_TARGET]


def enrich_candidates(candidates: List[Dict]) -> List[Dict]:
    out = []
    for idx, rec in enumerate(candidates, start=1):
        aid = rec["arxiv_id"]
        s2 = fetch_s2(aid)
        # Be nice to S2 rate limits.
        if idx % 5 == 0:
            time.sleep(1.2)

        s2_ext = s2.get("externalIds") or {}
        doi = s2_ext.get("DOI") if isinstance(s2_ext, dict) else None
        if isinstance(doi, list):
            doi = doi[0] if doi else None
        doi = doi if doi else "unknown"

        crossref_msg: Dict = {}
        crossref_url = ""
        if doi != "unknown":
            crossref_msg, crossref_url = fetch_crossref(doi)

        venue = infer_venue(s2, crossref_msg)
        citations = s2.get("citationCount")
        if not isinstance(citations, int):
            citations = None

        has_code = bool(rec.get("code_link")) or ("github.com" in (rec.get("summary", "").lower()))
        has_pdf = bool(rec.get("pdf_link"))

        v_score = venue_score(venue, citations, has_code)
        i_score = influence_score(citations)
        r_score = reproducibility_score(has_pdf, has_code)
        total = rec["relevance"] + v_score + i_score + r_score

        notes = []
        notes.append(f"relevance={rec['relevance']} from keyword groups: {','.join(rec['keyword_groups'])}")
        if venue == "unknown":
            notes.append("venue unknown from available metadata")
        if citations is None:
            notes.append("citations unknown from S2 response")
        elif rec["year"] >= 2025 and citations < 5:
            notes.append("early citation stage")
        if doi == "unknown":
            notes.append("doi unknown")

        source_links = [rec["arxiv_abs"], s2.get("_evidence_url")]
        if crossref_url:
            source_links.append(crossref_url)

        enriched = dict(rec)
        enriched.update(
            {
                "venue": venue,
                "doi": doi,
                "citations": citations if citations is not None else "unknown",
                "citations_num": citations if citations is not None else -1,
                "venue_score": v_score,
                "influence_score": i_score,
                "repro_score": r_score,
                "match_score_total": total,
                "match_score": f"{rec['relevance']}+{v_score}+{i_score}+{r_score}={total}",
                "notes": "; ".join(notes),
                "source_links": source_links,
                "s2_evidence_url": s2.get("_evidence_url"),
                "crossref_evidence_url": crossref_url if crossref_url else "",
                "buckets": bucket_tags(rec["keyword_groups"]),
            }
        )
        out.append(enriched)
    return out


def select_final(enriched: List[Dict]) -> List[Dict]:
    ranked = sorted(
        enriched,
        key=lambda x: (
            x["match_score_total"],
            x["relevance"],
            x["influence_score"],
            x["citations_num"],
            x["published"],
        ),
        reverse=True,
    )

    selected: List[Dict] = []
    selected_ids = set()
    for bucket in ["unlearning", "privacy_mia", "influence_retraining", "distill_partition"]:
        bucket_candidates = [p for p in ranked if bucket in p["buckets"] and p["arxiv_id"] not in selected_ids]
        if bucket_candidates:
            chosen = bucket_candidates[0]
            selected.append(chosen)
            selected_ids.add(chosen["arxiv_id"])

    for p in ranked:
        if len(selected) >= SELECTED_TARGET:
            break
        if p["arxiv_id"] in selected_ids:
            continue
        selected.append(p)
        selected_ids.add(p["arxiv_id"])

    # Enforce 8-12 requirement by clipping.
    if len(selected) < 8:
        selected = ranked[:8]
    if len(selected) > 12:
        selected = selected[:12]
    return selected


def write_csv(path: str, rows: List[Dict]) -> None:
    fieldnames = [
        "arxiv_id",
        "title",
        "year",
        "authors",
        "venue",
        "doi",
        "citations",
        "source_links",
        "keywords",
        "match_score",
        "notes",
        "local_path",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "arxiv_id": r["arxiv_id"],
                    "title": r["title"],
                    "year": r["year"],
                    "authors": "; ".join(r.get("authors", [])),
                    "venue": r.get("venue", "unknown"),
                    "doi": r.get("doi", "unknown"),
                    "citations": r.get("citations", "unknown"),
                    "source_links": " | ".join(r.get("source_links", [])),
                    "keywords": ",".join(r.get("keyword_groups", [])),
                    "match_score": r.get("match_score", ""),
                    "notes": r.get("notes", ""),
                    "local_path": r.get("local_path", ""),
                }
            )


def write_overview(candidates: List[Dict], selected: List[Dict]) -> None:
    selected_ids = {p["arxiv_id"] for p in selected}
    ts = dt.datetime.now(dt.timezone.utc).isoformat()
    lines: List[str] = []
    lines.append("# Graph Unlearning + GNN Paper Library (Reproducible Build)")
    lines.append("")
    lines.append(f"- Build time (UTC): `{ts}`")
    lines.append(f"- Priority window: `{CUTOFF_PRIORITY.date()} to now`")
    lines.append("- Metadata sources: arXiv + Semantic Scholar + Crossref (if DOI available)")
    lines.append("")
    lines.append("## Search Queries (arXiv)")
    lines.append("")
    for q in ARXIV_QUERIES:
        lines.append(f"- `{q}`")
    lines.append("")
    lines.append("## Scoring")
    lines.append("")
    lines.append("- relevance (0-3): keyword-group match to GU topics")
    lines.append("- venue gate (0-3): top venue > known venue > unknown")
    lines.append("- influence (0-3): Semantic Scholar citation count")
    lines.append("- reproducibility (0-2): PDF + code signal")
    lines.append("")
    lines.append("## Candidate Table (>=20)")
    lines.append("")
    lines.append("| # | arXiv | Year | Title | Scores (R+V+I+Rep) | Citations | Selected | Evidence |")
    lines.append("|---|---|---:|---|---|---:|---|---|")
    ranked_candidates = sorted(
        candidates,
        key=lambda x: (
            x["match_score_total"],
            x["relevance"],
            x["influence_score"],
            x["published"],
        ),
        reverse=True,
    )
    for i, p in enumerate(ranked_candidates, start=1):
        status = "yes" if p["arxiv_id"] in selected_ids else "no"
        s2_link = p["s2_evidence_url"]
        cr_link = p.get("crossref_evidence_url", "")
        ev = f"[arXiv]({p['arxiv_abs']}) / [S2]({s2_link})"
        if cr_link:
            ev += f" / [Crossref]({cr_link})"
        lines.append(
            f"| {i} | {p['arxiv_id']} | {p['year']} | {p['title']} | {p['match_score']} | "
            f"{p['citations']} | {status} | {ev} |"
        )
    lines.append("")
    lines.append("## Selected Papers (8-12)")
    lines.append("")
    for i, p in enumerate(selected, start=1):
        lines.append(f"### {i}. {p['arxiv_id']} - {p['title']}")
        lines.append(f"- score: `{p['match_score']}`")
        lines.append(f"- keywords: `{','.join(p.get('keyword_groups', []))}`")
        lines.append(f"- screening reason: {p['notes']}")
        lines.append(f"- evidence: [arXiv]({p['arxiv_abs']}), [S2]({p['s2_evidence_url']})" + (f", [Crossref]({p['crossref_evidence_url']})" if p.get("crossref_evidence_url") else ""))
        lines.append(f"- note card: `papers/notes/{p['arxiv_id']}.md`")
        lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("- `papers/papers.csv`")
    lines.append("- `papers/candidates.csv`")
    lines.append("- `papers/library.bib`")
    lines.append("- `papers/notes/*.md`")
    lines.append("- `papers/raw/*.json`")
    lines.append("")

    with open(os.path.join(BASE_DIR, "overview.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    ensure_dirs()

    arxiv_pool = fetch_arxiv_candidates()
    with open(os.path.join(RAW_DIR, "arxiv_pool.json"), "w", encoding="utf-8") as f:
        json.dump(arxiv_pool, f, ensure_ascii=False, indent=2)

    screened = screen_and_rank(arxiv_pool)
    if len(screened) < 20:
        raise RuntimeError(f"Screened candidates too few: {len(screened)} (<20)")

    candidates = enrich_candidates(screened)
    selected = select_final(candidates)

    # Download selected PDFs and write note cards.
    for p in selected:
        short = slugify_title(p["title"])
        pdf_name = f"{p['arxiv_id']}_{short}.pdf"
        pdf_path = os.path.join(BASE_DIR, pdf_name)
        ok = download_pdf(p["pdf_link"], pdf_path)
        if not ok:
            # Fallback to canonical link.
            fallback = f"https://arxiv.org/pdf/{p['arxiv_id']}.pdf"
            ok = download_pdf(fallback, pdf_path)
        p["local_path"] = f"papers/{pdf_name}" if ok else "unknown"

        note_path = os.path.join(NOTES_DIR, f"{p['arxiv_id']}.md")
        with open(note_path, "w", encoding="utf-8") as nf:
            nf.write(build_note(p))

    # For non-selected candidates, local path is blank.
    for p in candidates:
        if "local_path" not in p:
            p["local_path"] = ""

    with open(os.path.join(RAW_DIR, "candidates_enriched.json"), "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    with open(os.path.join(RAW_DIR, "selected.json"), "w", encoding="utf-8") as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

    write_csv(os.path.join(BASE_DIR, "candidates.csv"), candidates)
    write_csv(os.path.join(BASE_DIR, "papers.csv"), selected)

    with open(os.path.join(BASE_DIR, "library.bib"), "w", encoding="utf-8") as f:
        for p in selected:
            f.write(make_bib_entry(p))
            f.write("\n")

    write_overview(candidates, selected)

    print(f"Done. candidates={len(candidates)}, selected={len(selected)}")


if __name__ == "__main__":
    main()
