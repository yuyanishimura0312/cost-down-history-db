#!/usr/bin/env python3
"""Export DB to JSON for interactive web app."""

import sqlite3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "cdh.sqlite"
OUT = ROOT / "docs" / "data.json"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

methods = [dict(r) for r in c.execute("SELECT * FROM methods")]
evidence = [dict(r) for r in c.execute("SELECT * FROM evidence")]
genealogy = [dict(r) for r in c.execute("SELECT * FROM genealogy")]
critiques = [dict(r) for r in c.execute("SELECT * FROM critiques")]
domains = [dict(r) for r in c.execute("SELECT * FROM domains")]

data = {
    "version": "1.3",
    "updated": "2026-05-15",
    "stats": {
        "methods": len(methods),
        "evidence": len(evidence),
        "genealogy": len(genealogy),
        "critiques": len(critiques),
        "domains": len(domains),
    },
    "methods": methods,
    "evidence": evidence,
    "genealogy": genealogy,
    "critiques": critiques,
    "domains": domains,
}

OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
print(f"Exported: {OUT} ({OUT.stat().st_size:,} bytes)")

# Also export verification report
verification = {
    "total": len(methods),
    "verified": sum(1 for m in methods if m["verification"] == "verified"),
    "requires_review": sum(1 for m in methods if m["verification"] == "requires_review"),
    "requires_review_methods": [
        {"method_id": m["method_id"], "name_ja": m["name_ja"], "origin_country": m["origin_country"]}
        for m in methods if m["verification"] == "requires_review"
    ],
}
ver_out = ROOT / "docs" / "verification.json"
ver_out.write_text(json.dumps(verification, ensure_ascii=False, indent=2))
print(f"Verification: {ver_out}")
print(f"  verified: {verification['verified']}/{verification['total']} ({verification['verified']/verification['total']*100:.1f}%)")
print(f"  requires_review: {verification['requires_review']}")

conn.close()
