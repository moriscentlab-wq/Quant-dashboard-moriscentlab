"""
MQD Dashboard v1.0
Market Quant Dashboard
"""

import streamlit as st

from config.tickers import ALL_ASSETS
from collectors.yahoo import get_history

from indicators.moving_average import calculate_moving_average
from indicators.rsi import calculate_rsi
from scoring.mqd_score import calculate_mqd_score

from charts.price_chart import draw_price_chart
from utils.colors import (
    get_score_color,
    get_score_label,
)

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="MQD v1.0",
    page_icon="📈",
    layout="wide",
)

st.title("📈 MQD Dashboard v1.0")
st.caption("Market Quant Dashboard")

# ----------------------------------
# Sidebar
# ----------------------------------

market = st.sidebar.selectbox(
    "시장 선택",
    list(ALL_ASSETS.keys())
)

asset_name = st.sidebar.selectbox(
    "종목 선택",
    list(ALL_ASSETS[market].keys())
)

asset = ALL_ASSETS[market][asset_name]

st.sidebar.markdown("---")
st.sidebar.write(f"선택 종목 : **{asset.name}**")
st.sidebar.write(f"Ticker : `{asset.ticker}`")
