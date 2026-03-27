
**Primetrade.ai — Trader Performance vs Market Sentiment | Real Data**

---

## Methodology

**Datasets.** Two real datasets were used: (1) the Bitcoin Fear/Greed Index with 2,644 daily records spanning Feb 2018–May 2025, and (2) Hyperliquid historical trade data with 211,224 rows across 32 unique accounts from May 2023 to May 2025. Both datasets were perfectly clean — zero missing values, zero duplicates — requiring minimal pre-processing.

**Alignment.** The Hyperliquid timestamps were in IST (`DD-MM-YYYY HH:MM`) and required `dayfirst=True` parsing. After normalising to UTC midnight and inner-joining on date, the usable window became 479 trading days (May 2023–May 2025), retaining all 211,218 trades. Fear/Neutral/Extreme Fear days were grouped as "Fear"; Greed/Extreme Greed as "Greed" for binary comparisons.

**Feature engineering.** Trade-level flags were derived: is_win (Closed PnL > 0), is_long (Side == BUY), is_liquidation (Direction contains "Liquidat"). Net PnL was computed as `Closed PnL − Fee` to capture true profit after cost. Since Hyperliquid does not log leverage directly, a proxy was derived as `Size USD / |Start Position|` for closing trades. Per-account daily aggregates were built (daily PnL, win rate, trade count, long ratio, drawdown proxy via running max). A market-level daily table and lifetime trader summary were also produced. Three orthogonal segmentation axes were applied: leverage tier, trade frequency tier, and performance tier (each by tercile/quantile cut).

**Analysis.** Two-sample t-tests were used to test significance of sentiment-group differences. Pearson correlation across daily metrics quantified linear relationships. Segment × sentiment cross-tabs were compared to isolate which trader types respond most to sentiment shifts. For clustering, KMeans (k=4, elbow-selected) was applied to z-scored trader features. A Gradient Boosted Classifier (150 trees, depth=4, LR=0.05) was trained to predict next-day profitability from sentiment + behaviour features.

---

## Insights

**Insight 1 — Traders massively over-trade on Fear days (statistical significance: p < 0.01).**
Traders are **more active** on fear days.
Fear days see 103.7 trades/account/day versus 76.9 on Greed days — a 35% increase. Average position size is also 35% larger ($8,025 vs $5,955). Despite this hyperactivity, daily PnL is not meaningfully higher (p=0.72). The implication is clear: Fear-driven overtrading generates fees and execution noise without generating edge. Total fees are proportionally higher on Fear days, directly eroding PnL.

**Insight 2 — High-leverage traders have a Greed-regime advantage that low-leverage traders do not.**
Segmenting by leverage tier reveals a strong interaction: high-leverage traders average +$42.75/trade on Fear days but +$84.85 on Greed days — a 98% improvement. Low-leverage traders average +$29.67 (Fear) vs +$47.27 (Greed) — a 59% improvement. The leverage tier matters more on Greed days, suggesting momentum amplification works best in optimistic regimes but creates drag on volatile Fear days.

**Insight 3 — The best traders turn contrarian on Greed: long ratio drops from 50.6% to 47.2%.**
Contrary to retail behaviour (which crowds into longs on Greed), these sophisticated Hyperliquid traders shift toward neutral-to-short positioning as the Fear/Greed Index rises. This is a meaningful 3.4 percentage-point shift. The highest-PnL traders show the most pronounced version of this — they are selling the Greed, not riding it.

---

## Strategy Recommendations

**Rule 1 — Sentiment-Gated Frequency Control.**
On Fear days, reduce trade count by ~30%. The data shows that traders who fire more trades on Fear days are not earning more — they are paying more in fees while their win rate stays flat. A simple rule: if the daily FG Index < 40, set a daily trade cap 30% below your Greed-day average. This alone should improve net PnL on Fear days without changing entry logic.

**Rule 2 — Contrarian Bias at Sentiment Extremes.**
When FG Index > 70 (Greed/Extreme Greed): reduce long ratio below 50% — bias toward short or flat. The top performers in this dataset do this systematically, and their Greed-day returns are strongest precisely because they are not caught in long crowding. When FG Index < 30 (Extreme Fear): go long on pullbacks with tighter position sizing — fear-driven selling creates entries, but size control matters because drawdown is deepest in this zone. In both cases, the contrarian edge requires **patience over frequency**: fewer, larger, better-timed trades beat chasing every move.

---
## Key Takeaways
- Traders trade more during fear but are less profitable
- Larger trades correlate with higher risk
- Behavior patterns can predict outcomes moderately well

*Trader-specific behavior (risk, size, frequency) is far more influential.

---

**NOTE** : Prioritize consistent traders during volatile (fear) markets.