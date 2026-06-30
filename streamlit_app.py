"""
MQD v2 Streamlit Dashboard

Purpose
-------
- Visualize MQD Score system
- Multi-asset analysis
- Signal dashboard

This is the FINAL presentation layer.

Python 3.12
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config.tickers import ALL_ASSETS
from collectors.yahoo import get_history
from pipeline import run_mqd_pipeline
from scoring.mqd_score import calculate_mqd_score

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD v2 - Quant Dashboard")
st.caption("Research. Analyze. Decide.")

"""
MQD v2 Streamlit Dashboard

Purpose
-------
- Visualize MQD Score system
- Multi-asset analysis
- Signal dashboard

This is the FINAL presentation layer.

Python 3.12
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config.tickers import ALL_ASSETS
from collectors.yahoo import get_history
from pipeline import run_mqd_pipeline
from scoring.mqd_score import calculate_mqd_score

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD v2 - Quant Dashboard")
st.caption("Research. Analyze. Decide.")

# ==========================================================
# Run MQD Pipeline
# ==========================================================

mqd_output = run_mqd_pipeline(df)

data = mqd_output["data"]
state = mqd_output["state"]
snapshot = mqd_output["snapshot"]
flags = mqd_output["flags"]


# ==========================================================
# Calculate MQD Score
# ==========================================================

score_result = calculate_mqd_score(state)

mqd_score = score_result["mqd_score"]
mqd_signal = score_result["signal"]

trend_score = score_result["trend"]
momentum_score = score_result["momentum"]
flow_score = score_result["money_flow"]
volatility_score = score_result["volatility"]

# ==========================================================
# KPI Dashboard
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="MQD Score",
        value=f"{mqd_score:.2f}",
        delta=mqd_signal,
    )

with col2:
    st.metric(
        label="Trend Score",
        value=f"{trend_score:.2f}",
    )

with col3:
    st.metric(
        label="Momentum Score",
        value=f"{momentum_score:.2f}",
    )

with col4:
    st.metric(
        label="Money Flow",
        value=f"{flow_score:.2f}",
    )


# ==========================================================
# Volatility Panel
# ==========================================================

st.subheader("📉 Volatility & Risk")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Volatility Score",
        value=f"{volatility_score:.2f}",
    )

with col2:
    st.write("ATR (%)")
    st.write(snapshot.get("atr_pct", 0))


# ==========================================================
# Signal Summary
# ==========================================================

st.subheader("📊 Market Signal Summary")

st.markdown(f"""
### 🧠 MQD Signal: **{mqd_signal}**

- Trend: `{state.get("trend_bullish", False) and "Bullish" or "Bearish"}`
- MACD: `{state.get("macd_bullish", False) and "Bullish" or "Bearish"}`
- MFI: `{state.get("mfi", 50):.2f}`
- OBV: `{state.get("obv_rising", False) and "Rising" or "Falling"}`
- VWAP: `{state.get("above_vwap", False) and "Above" or "Below"}`
""")

# ==========================================================
# Price Chart (Plotly)
# ==========================================================

st.subheader("📈 Price Chart")

chart_df = data.copy()

fig = go.Figure()

# ==========================================================
# Price
# ==========================================================

fig.add_trace(
    go.Scatter(
        x=chart_df.index,
        y=chart_df["Close"],
        mode="lines",
        name="Close Price",
    )
)

# ==========================================================
# Moving Averages
# ==========================================================

if "SMA_20" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["SMA_20"],
            name="SMA 20",
        )
    )

if "SMA_60" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["SMA_60"],
            name="SMA 60",
        )
    )

# ==========================================================
# VWAP
# ==========================================================

if "VWAP" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["VWAP"],
            name="VWAP",
        )
    )

# ==========================================================
# Bollinger Bands
# ==========================================================

if "BB_Upper" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["BB_Upper"],
            name="BB Upper",
            line=dict(dash="dot"),
        )
    )

if "BB_Lower" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["BB_Lower"],
            name="BB Lower",
            line=dict(dash="dot"),
        )
    )

# ==========================================================
# Layout
# ==========================================================

fig.update_layout(
    title=f"{selected_asset} Price Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    height=600,
    legend=dict(orientation="h"),
)

st.plotly_chart(fig, use_container_width=True)
