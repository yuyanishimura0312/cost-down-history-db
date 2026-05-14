#!/usr/bin/env python3
"""Apply 5-team mechanism expansion to DB."""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "cdh.sqlite"
conn = sqlite3.connect(DB)
c = conn.cursor()

TSV_FILES = [
    ("/tmp/cdh_r1.tsv", "|"),
    ("/tmp/cdh_mechanism_updates_final.tsv", "\t"),  # R2
    ("/tmp/mechanism_updates.tsv", "|"),  # R3
    ("/tmp/cdh_r4.tsv", "|"),
    ("/tmp/cdh_mechanism_final.tsv", "|"),  # R5
]

stats = {"updated": 0, "skipped": 0, "not_found": []}

for path, sep in TSV_FILES:
    p = Path(path)
    if not p.exists():
        print(f"SKIP missing: {path}")
        continue
    lines = p.read_text(encoding="utf-8").strip().split("\n")
    print(f"\n=== {path} ({len(lines)} lines, sep={sep!r}) ===")
    for line in lines:
        if not line.strip() or not line.startswith("CDH-MET-"):
            continue
        parts = line.split(sep, 1)
        if len(parts) != 2:
            stats["skipped"] += 1
            continue
        mid, new_mech = parts
        mid = mid.strip()
        new_mech = new_mech.strip()
        if len(new_mech) < 50:
            stats["skipped"] += 1
            continue
        # Check exists
        r = c.execute("SELECT 1 FROM methods WHERE method_id = ?", (mid,)).fetchone()
        if not r:
            stats["not_found"].append(mid)
            continue
        c.execute("UPDATE methods SET mechanism = ? WHERE method_id = ?", (new_mech, mid))
        stats["updated"] += 1

conn.commit()

# Final stats
total = c.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
under_50 = c.execute("SELECT COUNT(*) FROM methods WHERE LENGTH(mechanism) < 50").fetchone()[0]
under_150 = c.execute("SELECT COUNT(*) FROM methods WHERE LENGTH(mechanism) < 150").fetchone()[0]
avg = c.execute("SELECT AVG(LENGTH(mechanism)) FROM methods").fetchone()[0]
max_len = c.execute("SELECT MAX(LENGTH(mechanism)) FROM methods").fetchone()[0]

print(f"\n=== Results ===")
print(f"Updated: {stats['updated']}")
print(f"Skipped: {stats['skipped']}")
print(f"Not found: {len(stats['not_found'])}")
if stats["not_found"]:
    print(f"  IDs: {stats['not_found'][:10]}")
print(f"\n=== Current state ===")
print(f"Total methods: {total}")
print(f"mechanism < 50 chars: {under_50}")
print(f"mechanism < 150 chars: {under_150}")
print(f"Average length: {avg:.1f}")
print(f"Max length: {max_len}")

conn.close()
