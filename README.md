#  Primetrade.ai — Trader Performance vs Market Sentiment
**Data Science Intern Assignment | Data Analysis**

> 211,224 trades · 32 Hyperliquid accounts · May 2023 – May 2025 · 479 trading days

---

## 📁 Structure

```
.
├── analysis.ipynb  
├── README.md
├── WRITEUP.md                            
│   ├── fear_greed_index.csv
│   └── historical_data.csv              
├── charts/   
                          
```

---

## Setup

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
# Place fear_greed_index.csv and historical_data.csv in data/
jupyter notebook Trader_Sentiment_Analysis_REAL.ipynb
```

---

##  Key Findings

| Metric | Fear Days | Greed Days | Δ |
|---|---|---|---|
| Avg Daily PnL | +$4,488 | +$4,067 | −$421 (not significant) |
| Win Rate | 35.65% | 36.27% | +0.6pp |
| Trades/Day | 103.7 | 76.9 | **−35%** ✅ significant |
| Avg Trade Size | $8,025 | $5,955 | **−$2,070** ✅ significant |
| Long Ratio | 50.6% | 47.2% | −3.4pp |

**These are REAL Hyperliquid traders (32 accounts, 211k+ trades).**

### Top 3 Insights
1. **Traders over-trade on Fear days** — 35% more trades, 35% larger sizes. More activity ≠ more profit.
2. **High-leverage traders nearly double their PnL on Greed days** ($42.75 → $84.85/trade). Leverage is a regime-specific amplifier.
3. **Sophisticated traders go neutral-to-short on Greed** — long ratio *drops* from 50.6% to 47.2% as market gets greedy. Contrarian edge.

### Strategy Rules
- **Rule 1:** On Fear days, reduce trade frequency by 30%. Churning generates fees without edge.
- **Rule 2:** On Greed days (FG > 70), bias toward neutral/short. The best performers here are contrarian, not momentum followers.
---
## Key Takeaways
- Traders trade more during fear but are less profitable
- Larger trades correlate with higher risk
- Behavior patterns can predict outcomes moderately well

*Trader-specific behavior (risk, size, frequency) is far more influential.

---

Streamlit Live demo:

https://fqsm9664a7oiyfjjrfh9br.streamlit.app/

----
