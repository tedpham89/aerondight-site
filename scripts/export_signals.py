"""Export the two unlabeled signal feeds for the Silver Alpha page.

silver.json — L24 entry crossings recomputed from analysis_scores (LT
crosses 7.50 with the sector-or-fund door, Energy/Utilities excluded).
gold.json   — V3 new-entrant BUY signals from the balanced paper account
(v3_paper_trades, action='BUY'; SKIP/already-held rows never create trade
rows, so no text parsing needed. bootstrap_backfill is set on every row
in this account and is therefore not usable as a filter — the date window
+ 60d dedupe do the work instead).

Feeds are cumulative, newest first, date + symbol only (deliberately no
other detail). A symbol already in a feed within the trailing 60 calendar
days is not re-added. Each run scans a small trailing window (default 5
trading days) so missed days self-heal; --seed-days N widens the window
for the one-time initial fill. Run daily by update-site-daily.bat.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
RESEARCH = SITE_ROOT.parent / "equity-research - v2" / "data"
MAIN_DB = RESEARCH / "equity_research.db"
V3_DB = RESEARCH / "v3_production.db"
OUT_DIR = SITE_ROOT / "src" / "data" / "signals"

PREFERRED = {"Industrials", "Information Technology", "Communication Services"}
EXCLUDED = {"Energy", "Utilities"}
LT_THRESHOLD, FUND_MIN = 7.50, 8.0
DEDUP_DAYS = 60
V3_BALANCED = "v3_new_top10_d5_m2_h15_paper"


def l24_crossings(lookback_days: int) -> list[tuple[str, str]]:
    """(date, symbol) for every L24 entry crossing in the last N score dates."""
    con = sqlite3.connect(f"file:{MAIN_DB}?mode=ro", uri=True)
    dates = [r[0] for r in con.execute(
        "SELECT DISTINCT date FROM analysis_scores ORDER BY date DESC LIMIT ?",
        (lookback_days + 1,))][::-1]
    if len(dates) < 2:
        con.close()
        return []
    ph = ",".join("?" * len(dates))
    rows = con.execute(
        f"""SELECT symbol, date, combined_score, fundamental_score
            FROM analysis_scores WHERE model_type='long_term'
            AND date IN ({ph})""", dates).fetchall()
    sector = dict(con.execute("SELECT symbol, sector FROM stock_meta"))
    con.close()

    by_sym: dict[str, dict[str, tuple]] = {}
    for sym, d, lt, fund in rows:
        by_sym.setdefault(sym, {})[d] = (lt, fund)
    out = []
    for sym, per_date in by_sym.items():
        sec = sector.get(sym) or "Unknown"
        if sec in EXCLUDED:
            continue
        for i in range(1, len(dates)):
            prev, cur = per_date.get(dates[i - 1]), per_date.get(dates[i])
            if not prev or not cur:
                continue
            lt_prev, _ = prev
            lt, fund = cur
            if lt_prev is None or lt is None or fund is None:
                continue
            if not (lt_prev < LT_THRESHOLD <= lt):
                continue
            if sec not in PREFERRED and fund < FUND_MIN:
                continue
            out.append((dates[i], sym))
    return out


def v3_buys(lookback_days: int) -> list[tuple[str, str]]:
    """(signal_date, symbol) for balanced-account BUY signals."""
    cutoff = (date.today() - timedelta(days=lookback_days * 2)).isoformat()
    con = sqlite3.connect(f"file:{V3_DB}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT signal_date, symbol FROM v3_paper_trades
           WHERE portfolio_name=? AND action='BUY'
             AND signal_date >= ?""", (V3_BALANCED, cutoff)).fetchall()
    con.close()
    return [(d, s) for d, s in rows]


def update_feed(path: Path, new_items: list[tuple[str, str]]) -> int:
    feed = {"signals": []}
    if path.exists():
        feed = json.loads(path.read_text(encoding="utf-8"))
    existing = feed["signals"]
    added = 0
    for d, sym in sorted(new_items):
        disp = sym.replace(".US", "")
        dt = date.fromisoformat(d)
        dup = any(e["symbol"] == disp
                  and abs((dt - date.fromisoformat(e["date"])).days) <= DEDUP_DAYS
                  for e in existing)
        if dup:
            continue
        existing.append({"date": d, "symbol": disp})
        added += 1
    existing.sort(key=lambda e: (e["date"], e["symbol"]), reverse=True)
    path.write_text(json.dumps(feed, indent=1) + "\n", encoding="utf-8")
    return added


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-days", type=int, default=5,
                    help="Trailing trading-day window to scan (default 5)")
    args = ap.parse_args()
    if not MAIN_DB.exists() or not V3_DB.exists():
        print("[signals] research DBs not found", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_silver = update_feed(OUT_DIR / "silver.json", l24_crossings(args.seed_days))
    n_gold = update_feed(OUT_DIR / "gold.json", v3_buys(args.seed_days))
    print(f"[signals] silver +{n_silver}, gold +{n_gold}")
    return 0


if __name__ == "__main__":
    main()
