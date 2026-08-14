#!/usr/bin/env python3
"""Audit a canonical organizational roster CSV using only the standard library."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = [
    "Roster Record ID", "Formal Organization Name", "Organization Type",
    "Official Website URL", "Quick Mission / Role", "Prominence Tier",
    "Primary Evidence URL", "Evidence Checked Date", "Confidence",
]
ALLOWED_MISSING = {"Not publicly located", "Not applicable", "Unclear", "Needs review"}

def valid_url(value):
    p = urlparse(value.strip())
    return p.scheme in {"http", "https"} and bool(p.netloc)

def audit(path):
    errors, warnings, ids, names = [], [], set(), set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for col in REQUIRED:
            if col not in headers:
                errors.append(f"Missing required column: {col}")
        rows = list(reader)
    for i, row in enumerate(rows, start=2):
        rid = row.get("Roster Record ID", "").strip()
        name = row.get("Formal Organization Name", "").strip()
        if not rid: errors.append(f"Row {i}: blank Roster Record ID")
        elif rid in ids: errors.append(f"Row {i}: duplicate Roster Record ID {rid}")
        ids.add(rid)
        if not name: errors.append(f"Row {i}: blank Formal Organization Name")
        elif name.casefold() in names: warnings.append(f"Row {i}: repeated organization name {name}")
        names.add(name.casefold())
        for col in ["Official Website URL", "Primary Evidence URL"]:
            value = row.get(col, "").strip()
            if not value: errors.append(f"Row {i}: blank {col}")
            elif value not in ALLOWED_MISSING and not valid_url(value): errors.append(f"Row {i}: invalid {col}: {value}")
        for col in REQUIRED:
            if not row.get(col, "").strip(): errors.append(f"Row {i}: blank {col}")
        if row.get("Confidence", "").strip() not in {"High", "Medium", "Low"}:
            errors.append(f"Row {i}: invalid Confidence")
    return {"file": str(path), "rows": len(rows), "errors": errors, "warnings": warnings, "pass": not errors}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--output", help="Write JSON audit to this path")
    args = ap.parse_args()
    result = audit(Path(args.csv_path))
    payload = json.dumps(result, indent=2)
    if args.output: Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    raise SystemExit(0 if result["pass"] else 1)
