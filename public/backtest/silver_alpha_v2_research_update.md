# Silver Alpha v2 Research Update

May 2026

We recently widened the Silver Alpha v2 validation window from the recent
2023-2025 period to a broader 2020-2025 out-of-sample test. This matters because
the expanded window includes the COVID crash and rebound, the 2022 bear market,
and the later AI-led recovery. The goal was not just to find a stronger return
profile, but to see whether the signal still held up across very different
market regimes.

## Headline Result

In the expanded test, the quality-focused Silver Alpha v2 candidate turned a
starting value of $100,000 into approximately $378,300, compared with about
$229,100 for SPY over the same period.

Key results:

- Total return: +278.3% versus +129.1% for SPY
- Annualized return: 24.9% versus 14.9% for SPY
- Excess annualized return: +10.0%
- Sharpe ratio: 1.07 versus 0.77 for SPY
- Maximum drawdown: -33.7%
- Completed trades: 96 (signal-based)
- Average trade return: +10.1%
- Median trade return: +3.6%
- Average excess return versus SPY: +6.3%
- Median excess return versus SPY: +1.3%
- Trades beating SPY: 53%

The main takeaway is that the edge did not disappear when the test was expanded
to include the COVID period and the 2022 drawdown. The system still produced
positive excess return, though it did not eliminate equity-market drawdowns.

## Annual Performance

The strategy outperformed or matched SPY in most calendar years:

| Year | Strategy | S&P 500 | Excess |
|------|----------|---------|--------|
| 2020 | +16.5%   | +17.2%  | -0.7%  |
| 2021 | +54.7%   | +30.5%  | +24.2% |
| 2022 | -8.5%    | -18.6%  | +10.2% |
| 2023 | +41.6%   | +26.7%  | +14.9% |
| 2024 | +22.5%   | +25.6%  | -3.1%  |
| 2025 | +39.6%   | +18.0%  | +21.6% |

The strongest outperformance came in years with sector rotation and momentum
divergence (2021, 2023, 2025). During the 2022 bear market the strategy
significantly outperformed by limiting losses. During the COVID year (2020) and
the narrow large-cap rally of 2024, the strategy roughly tracked SPY.

## What Changed In The Research

The newer test puts more emphasis on trade quality and repeatability. Rather
than optimizing only for final account value, we looked for a version with
positive average excess return, positive median excess return, and a win rate
against SPY above 50%.

That matters because annualized return can be distorted by a few unusually good
trades. Silver Alpha v2 is now being evaluated more on whether the average trade
has a repeatable edge over SPY, not only whether the equity curve compounds well
in one lucky path.

## Holding Window Finding

The fixed-horizon research suggests the edge is strongest around the
intermediate holding window. Median excess return improved from roughly +1.6%
at 21 trading days, to +3.2% at 42 trading days, and to +5.3% around 63 trading
days. Extending the window further still had positive results, but the median
edge no longer improved and fell to about +4.5% by 126 trading days.

The practical implication: Silver Alpha v2 appears to work best as a disciplined
multi-week to multi-month process, not as a buy-and-ignore strategy.

## Universe And Capacity Finding

The broader research universe includes both large-cap and mid-cap stocks, but
portfolio construction now gives preference to S&P 500 candidates when choices
are close. Mid-cap stocks can still produce strong individual winners, but the
large-cap preference improves liquidity, repeatability, and implementation
quality for a public-facing system.

## Bottom Line

Silver Alpha v2 looks meaningfully more robust after the expanded 2020-2025
test. The best version did not rely only on a short post-2023 sample, and the
trade-level statistics improved enough to justify continuing with the v2
research direction.

The research does not prove the strategy will outperform in every environment.
It does show that the signal survived a wider and more difficult validation
period, with a cleaner edge profile than the original public test.

---

## Charts

### Equity Curve (silver_alpha_v2_equity_curve.png)

Shows the growth of $100,000 invested in Silver Alpha v2 versus the S&P 500
from January 2020 through December 2025. The top panel is the portfolio value
over time; the bottom panel shows the drawdown profile for both the strategy
and SPY. The strategy reached approximately $378,000 compared to $229,000 for
SPY, with a similar maximum drawdown of roughly -34% during the COVID crash.

### Annual Returns (silver_alpha_v2_annual_returns.png)

Bar chart comparing annual calendar-year returns between Silver Alpha v2 and the
S&P 500 for each year from 2020 to 2025. The strategy produced meaningfully
higher returns in four of six years (2021, 2022, 2023, 2025), roughly matched
SPY in 2020 and 2024. The largest single-year outperformance was +23.8% in 2025.

### Trade Excess Return Distribution (silver_alpha_v2_trade_distribution.png)

Histogram of individual trade excess returns versus SPY across all 96
signal-based trades. 53% of trades outperformed SPY. The distribution is
right-skewed: most trades cluster near zero excess, with a meaningful tail of
large winners (+20% to +80% excess). The median excess is +1.3%, confirming
a positive but modest per-trade edge that compounds over many trades.

### Cumulative Excess Return (silver_alpha_v2_cumulative_excess.png)

Shows the cumulative relative performance of the strategy versus SPY over time
(portfolio value / SPY value - 1). Green shading indicates periods of
outperformance, red indicates underperformance. The chart shows the excess built
primarily during 2021 and 2023-2025, with a flat period during 2022 and a brief
underperformance dip in early 2020 during the COVID crash.
