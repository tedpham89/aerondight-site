"""Export weekly sector rotation summaries for the website.

Reads the official weekly signals from the research repo's rotation paper DB
(rotation_signals, run_type='official') and writes one small JSON per week to
src/data/rotation/YYYY-MM-DD.json. Only the public summary is exported:
regime + vote count, sectors freshly rotating IN, sectors freshly rotating
OUT. No momentum leaders / basket tickers.

Idempotent: writes any week missing from src/data/rotation, never rewrites
existing files (a published week is frozen). Run by scripts/update-rotation.bat
every Saturday, followed by git commit + push (Cloudflare Pages auto-deploys).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
PAPER_DB = (SITE_ROOT.parent / "equity-research - v2" / "data" /
            "rotation_paper.db")
OUT_DIR = SITE_ROOT / "src" / "data" / "rotation"

IN_STATE = "CONFIRMED IN (fresh)"
OUT_STATE = "CONFIRMED OUT (fresh)"


def export() -> int:
    if not PAPER_DB.exists():
        print(f"[export] paper DB not found: {PAPER_DB}", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(f"file:{PAPER_DB}?mode=ro", uri=True)
    try:
        weeks = [r[0] for r in con.execute(
            "SELECT DISTINCT week_end FROM rotation_signals "
            "WHERE run_type='official' ORDER BY week_end")]
        written = 0
        for week_end in weeks:
            out_path = OUT_DIR / f"{week_end}.json"
            if out_path.exists():
                continue
            rows = con.execute(
                "SELECT sector, state, regime, votes_on FROM rotation_signals "
                "WHERE run_type='official' AND week_end=? ORDER BY sector",
                (week_end,)).fetchall()
            regime, votes_on = rows[0][2], rows[0][3]
            payload = {
                "week_end": week_end,
                "regime": regime,
                "votes_on": votes_on,
                "votes_total": 5,
                "rotation_in": [s for s, st, _, _ in rows if st == IN_STATE],
                "rotation_out": [s for s, st, _, _ in rows if st == OUT_STATE],
            }
            out_path.write_text(json.dumps(payload, indent=2) + "\n",
                                encoding="utf-8")
            print(f"[export] wrote {out_path.name}: {regime} "
                  f"({votes_on}/5), in={payload['rotation_in'] or '-'}, "
                  f"out={payload['rotation_out'] or '-'}")
            written += 1
        if not written:
            print(f"[export] up to date ({len(weeks)} weeks already exported).")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(export())
