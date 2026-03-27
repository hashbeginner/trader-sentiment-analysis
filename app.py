import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Primetrade.ai — Sentiment Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    # Load sentiment data
    fg = pd.read_csv("data/fear_greed_index.csv")

    # Auto-detect date column
    for col in ['date', 'Date', 'timestamp']:
        if col in fg.columns:
            fg['date'] = pd.to_datetime(fg[col]).dt.normalize()
            break

    fg = fg.drop_duplicates('date')

    # Standardize sentiment
    fg['sentiment'] = fg['classification'].apply(
        lambda x: "Greed" if "Greed" in x else "Fear"
    )

    # Load trade data
    trd = pd.read_csv("data/historical_data.csv")

    # Fix timestamp column
    if "Timestamp IST" in trd.columns:
        trd['datetime'] = pd.to_datetime(trd['Timestamp IST'], dayfirst=True)
    else:
        st.error("❌ Timestamp column not found")
        st.stop()

    trd['date'] = trd['datetime'].dt.normalize()

    # Feature engineering
    trd['net_pnl'] = trd['Closed PnL'] - trd['Fee']
    trd['is_win'] = (trd['Closed PnL'] > 0).astype(int)
    trd['is_long'] = (trd['Side'] == 'BUY').astype(int)

    # Merge
    df = pd.merge(trd, fg[['date', 'classification', 'sentiment']], on='date')

    return df


df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Filters")

sentiments = st.sidebar.multiselect(
    "Sentiment",
    options=df['classification'].unique(),
    default=df['classification'].unique()
)

df = df[df['classification'].isin(sentiments)]

# ---------------- METRICS ----------------
st.title("📊 Trader Sentiment Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Trades", len(df))
col2.metric("Average PnL", f"${df['net_pnl'].mean():.2f}")
col3.metric("Win Rate", f"{df['is_win'].mean()*100:.2f}%")

# ---------------- PNL BY SENTIMENT ----------------
st.subheader("📊 PnL by Sentiment")

pnl = df.groupby('sentiment')['net_pnl'].mean()

fig = px.bar(
    x=pnl.index,
    y=pnl.values,
    labels={'x': 'Sentiment', 'y': 'Avg PnL'},
    color=pnl.index
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- TRADES OVER TIME ----------------
st.subheader("📈 Trades Over Time")

trades = df.groupby('date').size()

fig = px.line(
    x=trades.index,
    y=trades.values,
    labels={'x': 'Date', 'y': 'Trades'}
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- LEVERAGE (if exists) ----------------
if "Size USD" in df.columns and "Start Position" in df.columns:
    df['leverage'] = df['Size USD'] / (df['Start Position'].abs() + 1)

    st.subheader("⚡ Leverage Distribution")

    fig = px.histogram(df, x='leverage', nbins=30)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- LONG / SHORT ----------------
st.subheader("📉 Long vs Short")

ls = df.groupby(['sentiment', 'Side']).size().unstack().fillna(0)
st.dataframe(ls)

# ---------------- SEGMENTATION ----------------
st.subheader("🧩 Segmentation (High vs Low PnL)")

df['segment'] = df['net_pnl'].apply(lambda x: 'High' if x > 0 else 'Low')

seg = df.groupby('segment')['net_pnl'].mean()

fig = px.bar(x=seg.index, y=seg.values)
st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("💡 Insights")

st.markdown("""
- Traders are more active during Fear periods.
- Higher leverage increases volatility.
- Greed periods show higher average returns but higher risk.
""")