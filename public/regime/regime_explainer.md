# Market Regime Classification

Aerondight Systems uses a Hidden Markov Model (HMM) to classify the current market
environment into one of four distinct states. An independent XGBoost classifier
validates the HMM's output — when both models agree, signal confidence increases.

## The Four Regimes

### Bull Broad
The real economy is rallying with broad market participation. Cyclical sectors
outperform, breadth is strong, and volatility is low. This is the classic
risk-on environment where most stocks participate in the uptrend.

### Bull Tech
A tech-led, narrow rally. Large-cap technology drives returns while breadth
is weaker. VIX remains low, but leadership is concentrated. Momentum strategies
work well, but the narrow base creates fragility.

### Correction
A grinding bear market with elevated volatility (~24 VIX). Breadth deteriorates,
spreads widen, and defensive sectors begin to outperform. This regime can persist
for months and often precedes either recovery or deeper crisis.

### Crisis
A sharp, violent crash with extreme volatility (~45 VIX). This is rare (~6% of
historical time) but devastating. Correlations spike toward 1.0, and traditional
diversification fails. These episodes are short-lived but create the best
long-term buying opportunities for patient investors.

## How It Works

The HMM learns the statistical properties of each regime from historical macro
data — it identifies clusters of similar market behavior without being told
what to look for. State labels (bull_broad, bull_tech, correction, crisis) are
assigned automatically after training based on the return and risk characteristics
of each cluster.

The XGBoost validator independently predicts the regime using a broader set of
features. When both models agree, the system has higher confidence in the
current regime classification.

The regime classification feeds into the scoring engine — the same stock can
receive different scores depending on whether the market is in a broad bull
rally or a grinding correction.
