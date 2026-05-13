#!/usr/bin/env python3
"""Fix WARN items from VALIDATION_REPORT: replace failing URLs with Wayback, fix genealogy year."""

import sqlite3
import urllib.request
import urllib.parse
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DB = Path(__file__).resolve().parent.parent / "cdh.sqlite"

FAILING_URLS = [
    "https://asq.org/quality-resources/dmaic",
    "https://direct.mit.edu/books/monograph/1856/Design-Rules-Volume-1The-Power-of-Modularity",
    "https://tech.slashdot.org/story/19/01/05/0248207/what-happened-when-automation-came-to-general-motors",
    "https://www.bcg.com/ja-jp/increase-resilience-global-supply-chain",
    "https://www.bcg.com/publications/1968/business-unit-strategy-growth-experience-curve",
    "https://www.ecr-community.org/",
    "https://www.iea.org/",
    "https://www.innocentive.com/",
    "https://www.netsuite.com/portal/resource/articles/erp/distribution-requirement-planning-drp.shtml",
    "https://www.projectmanagement.com/blog-post/412/does-six-sigma-kill-creativity-",
    "https://www.tandfonline.com/doi/abs/10.1080/00207540050031823",
    "https://www.value-eng.org/",
    "https://www.value-eng.org/page/ValueStandards",
    "https://sortly.com/blog/rfid-vs-barcode-for-inventory-tracking",
    "https://www.2-data.com/knowledge-hub/a-history-of-salesforce",
    "https://www.schrodinger.com/life-science/learn/white-papers/reversing-erooms-law-can-computers-dramtically-impact-productivity-drug-discovery/",
    "https://www.srgresearch.com/articles/cloud-market-jumped-to-330-billion-in-2024",
    "https://www.computerhistory.org/siliconengine/scaling-of-ic-process-design-rules-quantified/",
    "https://corporate.ford.com/articles/history/the-model-t/",
    "https://indianote.asia/india-it-big3",
    "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-return-of-zero-base-budgeting",
]


def wayback_lookup(url):
    """Query Wayback Machine for archived version."""
    api = f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}"
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0 CDH-Validator"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            snap = data.get("archived_snapshots", {}).get("closest", {})
            if snap.get("available"):
                return url, snap.get("url")
    except Exception as e:
        return url, None
    return url, None


# Lookup in parallel
replacements = {}
with ThreadPoolExecutor(max_workers=16) as ex:
    futures = {ex.submit(wayback_lookup, u): u for u in FAILING_URLS}
    for f in as_completed(futures):
        orig, wb = f.result()
        if wb:
            replacements[orig] = wb
            print(f"OK   {orig[:60]}... -> Wayback")
        else:
            print(f"SKIP {orig[:60]}... no archive")

print(f"\nReplacements: {len(replacements)}/{len(FAILING_URLS)}")

# Apply to DB
conn = sqlite3.connect(DB)
c = conn.cursor()
updated = 0
for orig, wb in replacements.items():
    for table, col in [
        ("methods", "primary_source_url"),
        ("evidence", "source_url"),
        ("critiques", "source_url"),
    ]:
        n = c.execute(f"UPDATE {table} SET {col} = ? WHERE {col} = ?", (wb, orig)).rowcount
        updated += n

# Fix CDH-REL-0033: Wright曲線 → Li-ion学習曲線 was set to year_transition=2010 but child.era_start=1991
# The relationship "Wright (1936) inspires Li-ion learning curve (1991)" should have year_transition 1991 not 2010
# However the more accurate transition year is when Li-ion learning curve started being formally tracked: ~2010
# Actually the child era_start was set to 1991 (商用化). Let's set year_transition to 1991 to match the formal start.
n = c.execute("UPDATE genealogy SET year_transition = 1991, rationale = ? WHERE rel_id = 'CDH-REL-0033'",
              ("Wright曲線 → Li-ion 学習曲線（Sony 1991 商用化以降の累積生産でWright則を確認）",)).rowcount
print(f"Fixed CDH-REL-0033 genealogy year ({n} row)")
updated += n

conn.commit()
print(f"\nTotal rows updated: {updated}")
conn.close()
