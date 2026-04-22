# Aerondight Systems — Public Content Plan

What goes on aerondight.systems. Everything in this folder is safe to publish.

---

## architecture/ — DONE (auto-generated)
Simplified 3-layer diagram (no weights, no sub-pillar breakdowns):
- `architecture.md` — Mermaid diagram: Regime Classifier → Swing/LT Models → Signal Output

DO NOT INCLUDE: pillar weights (35/40/25, 50/25/25), sub-pillar breakdowns

## backtest/ — DONE (auto-generated)
Performance numbers (prove it works without revealing how):
- `quintile_returns.png` — Monotonic Q1-Q5 bar chart for both models (2020-2026 OOS)
- `performance_summary.png` — Summary card with signal quality + portfolio stats
- `silver_alpha_equity_curve.png` — Equity curve: Silver Alpha vs SPY (2023-2025)
- `silver_alpha_trades_2023_2025.csv` — 135 trades with entry/exit dates, prices, returns, exit reason

Trade log columns: symbol, entry_date, exit_date, entry_price, exit_price, return_pct, spy_return_pct, excess_pct, days_held, exit_reason

DO NOT INCLUDE: internal scores, pillar breakdowns, entry/exit threshold values

## regime/ — DONE (auto-generated)
The regime classifier story:
- `regime_explainer.md` — 4 states described conceptually + how HMM/XGBoost work together
- `regime_timeline.png` — SPY price with color-coded regime background (smoothed)

DO NOT INCLUDE: 7 HMM features, 31 XGBoost features, alignment mechanics

## tech-stack/ — DONE (auto-generated)
- `overview.md` — Python, SQLite, EODHD, Claude API, ~900 stocks, operational discipline

## thesis/ — MANUAL (run notebook 07)
Sample AI research report:
- Pick a well-known stock (AAPL or NVDA)
- Run notebook 07 with that ticker
- Copy the PDF to `public/thesis/`
- Redact any sub-score labels like [Val/Qual/Grow/BS] if visible

DO NOT INCLUDE: system prompt, raw sub-scores with pillar labels

---

## How to regenerate all auto-generated content
```bash
python public/generate_charts.py
```
This regenerates everything except the thesis PDF (~3 min for Silver Alpha simulation).

## Manual steps
1. Run notebook `07_ai_thesis.ipynb` for AAPL or NVDA
2. Copy the output PDF to `public/thesis/`
3. Review all charts visually before publishing

---

## NEVER PUBLISH (the edge)
- Pillar weights (top-level or sub-pillar)
- Scoring formulas (tanh sensitivity, MACD percentile, BB%B buckets)
- Percentile method (40% history + 60% peers)
- Signal thresholds (7.0 BUY, 5.0 SELL)
- Silver Alpha entry/exit rules (LT cross 7.5, tech >= 6.5, E16, 63d stale)
- Regime alignment/agreement modulation logic
- Transition predictor details (P(negative) > 40%, features)
- Position sizing rules, options strategy specifics (delta/spread)
- System prompt for AI thesis
