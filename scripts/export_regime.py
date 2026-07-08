"""Export the current HMM/XGBoost regime for the website's Regime tab.

Reads the latest row of regime_states from the research repo's main DB
(written nightly by after-hour.bat) and writes src/data/regime/current.json.
Overwrites daily - the page shows only the current state; history stays in
the research DB. Pushed by scripts/update-site-daily.bat (commit only fires
when the JSON actually changed).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
MAIN_DB = (SITE_ROOT.parent / "equity-research - v2" / "data" /
           "equity_research.db")
OUT = SITE_ROOT / "src" / "data" / "regime" / "current.json"


def main() -> int:
    if not MAIN_DB.exists():
        print(f"[regime] research DB not found: {MAIN_DB}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{MAIN_DB}?mode=ro", uri=True)
    row = con.execute(
        "SELECT date, hmm_regime_label, regime_agreement, xgb_confidence "
        "FROM regime_states ORDER BY date DESC LIMIT 1").fetchone()
    con.close()
    if not row:
        print("[regime] no regime_states rows", file=sys.stderr)
        return 1
    payload = {
        "date": row[0],
        "label": row[1],
        "agreement": bool(row[2]),
        "confidence": round(float(row[3]), 2),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    new = json.dumps(payload, indent=1) + "\n"
    if new == old:
        print(f"[regime] unchanged ({payload['date']} {payload['label']}).")
    else:
        OUT.write_text(new, encoding="utf-8")
        print(f"[regime] wrote {payload['date']} {payload['label']} "
              f"({'agree' if payload['agreement'] else 'disagree'}, "
              f"{payload['confidence']:.0%})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
