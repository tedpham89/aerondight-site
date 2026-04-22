# Tech Stack & Operations

## Platform
- **Language:** Python
- **Database:** SQLite (~2.5M price records, ~80K fundamental records)
- **Data Provider:** EODHD (end-of-day prices, fundamentals, macro indicators)
- **AI Integration:** Claude API (Sonnet) for institutional-quality research reports
- **Deployment:** Runs daily as a production scoring pipeline, not a notebook experiment

## Universe
- ~900 stocks scored daily (S&P 500 + S&P 400 MidCap)
- 19 macro/market tickers for regime classification
- 31 macro features computed from raw market data
- Price history back to 2006 for robust model training

## Scoring Engine
- Multi-factor scoring across fundamental, technical, and sector dimensions
- Each stock receives a conviction score (1-10) and a signal (BUY / WATCH / SELL)
- Two parallel models: Swing Trade (1-3 months) and Long Term (1+ year)
- Regime-aware: market conditions modulate scoring behavior

## Regime Classifier
- Hidden Markov Model (HMM) identifies current market regime from macro features
- XGBoost classifier validates HMM output independently
- Agreement between models increases signal confidence
- Four distinct market states detected and labeled automatically

## AI Research Reports
- Single-ticker, on-demand institutional-quality equity research
- Claude API generates 7-section analysis from quantitative signals + fundamental data + recent news
- Output: professional PDF with score history, color-coded signals, and disclaimer
- Cost: ~$0.005 per report

## Operational Discipline
- **Daily (after close):** Update prices, score all stocks, check entry/exit signals
- **Weekly:** Update fundamentals, plan trades based on signal transitions
- **Quarterly:** Retrain regime models on expanding window (never drop old data)
- Signal transitions matter more than static signals: WATCH->BUY is an entry trigger
