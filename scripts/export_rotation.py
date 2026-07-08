"""Export weekly sector rotation summaries for the website.

Reads the official weekly signals from the research repo's rotation paper DB
(rotation_signals, run_type='official') and writes one small JSON per week to
src/data/rotation/YYYY-MM-DD.json. Only the public summary is exported:
regime + vote count, sectors freshly rotating IN, sectors freshly rotating
OUT. No momentum leaders / basket tickers.

Idempotent: writes any week missing from src/data/rotation, never rewrites
existing files (a published week is frozen). Run by scripts/update-rotation.bat
every Saturday, followed by git commit + push (Cloudflare Pages auto-deploys).

--history N additionally exports the last N completed weeks from the
research repo's point-in-time backfill rows (run_type='backfill', replayed
2008-present with no lookahead). Official rows win where both exist.
Used once 2026-07-08 to seed the site with 10 weeks of history; the
Saturday automation runs without it (official weeks only).
"""
from __future__ import annotations

import argparse
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


def export(history_weeks: int = 0) -> int:
    if not PAPER_DB.exists():
        print(f"[export] paper DB not found: {PAPER_DB}", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(f"file:{PAPER_DB}?mode=ro", uri=True)
    try:
        weeks = {w: "official" for (w,) in con.execute(
            "SELECT DISTINCT week_end FROM rotation_signals "
            "WHERE run_type='official'")}
        if history_weeks:
            for (w,) in con.execute(
                    "SELECT DISTINCT week_end FROM rotation_signals "
                    "WHERE run_type='backfill' ORDER BY week_end DESC LIMIT ?",
                    (history_weeks,)):
                weeks.setdefault(w, "backfill")
        written = 0
        for week_end in sorted(weeks):
            out_path = OUT_DIR / f"{week_end}.json"
            if out_path.exists():
                continue
            rows = con.execute(
                "SELECT sector, state, regime, votes_on FROM rotation_signals "
                "WHERE run_type=? AND week_end=? ORDER BY sector",
                (weeks[week_end], week_end)).fetchall()
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", type=int, default=0,
                    help="Also export the last N weeks from backfill rows")
    args = ap.parse_args()
    sys.exit(export(history_weeks=args.history))
