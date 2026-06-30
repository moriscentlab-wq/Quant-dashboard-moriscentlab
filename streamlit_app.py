"""
MQD Dashboard v1.0
"""

import streamlit as st
import pandas as pd

from config.tickers import ALL_ASSETS
from collectors.yahoo import (
    get_history,
    get_last_update,
)

from indicators.moving_average import calculate_moving_average
from indicators.rsi import calculate_rsi
from scoring.mqd_score import calculate_mqd_score

from charts.price_chart import draw_price_chart
from utils.colors import (
    get_score_color,
    get_score_label,
)

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD Dashboard")
st.caption("Moris Quant Dashboard")
st.divider()

ranking = []

st.subheader("🌍 Global Market")

for category, assets in ALL_ASSETS.items():

    with st.expander(category, expanded=False):

        for asset in assets.values():

            try:

                history = get_history(asset.ticker)

                if history.empty:
                    st.warning(f"{asset.name} 데이터를 가져오지 못했습니다.")
                    continue

                history = calculate_moving_average(history)
                history = calculate_rsi(history)
                history = calculate_mqd_score(history)

                latest = history.iloc[-1]
                previous = history.iloc[-2]
