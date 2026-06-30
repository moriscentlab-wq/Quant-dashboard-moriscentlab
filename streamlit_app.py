"""
MQD Dashboard v1.0
Main Streamlit Application
"""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

from charts.price_chart import draw_price_chart
from collectors.yahoo import (
    get_history,
    get_last_update,
)
from config.tickers import ALL_ASSETS
from indicators.momentum import (
    calculate_momentum,
    calculate_rate_of_change,
)
from indicators.moving_average import (
    calculate_moving_average,
)
from indicators.rsi import (
    calculate_rsi,
)
from scoring.mqd_score import (
    calculate_mqd_score,
)
from utils.colors import (
    get_score_color,
    get_score_label,
)

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD Dashboard")
st.caption("Mori Quant Investing")

st.divider()


@st.cache_data(ttl=300)
def load_history(
    ticker: str,
) -> pd.DataFrame:

    return get_history(ticker)


# ------------------------------
# Sidebar
# ------------------------------

st.sidebar.header("MQD Dashboard")

market = st.sidebar.selectbox(
    "Market",
    list(ALL_ASSETS.keys()),
)

assets = ALL_ASSETS[market]

asset_name = st.sidebar.selectbox(
    "Ticker",
    list(assets.keys()),
)

asset = assets[asset_name]

st.sidebar.write("---")

st.sidebar.write(f"**Name** : {asset.name}")

st.sidebar.write(f"**Ticker** : {asset.ticker}")

download = st.sidebar.button(
    "Download Data",
    use_container_width=True,
)

# ----------------------------------------------------------
# Download
# ----------------------------------------------------------

if download:

    try:

        history = load_history(asset.ticker)

        if history.empty:
            st.error("데이터를 불러오지 못했습니다.")
            st.stop()

        # -------------------------------------
        # Indicators
        # -------------------------------------

        history = calculate_moving_average(
            history
        )

        history = calculate_rsi(
            history
        )

        history = calculate_rate_of_change(
            history
        )

        history = calculate_momentum(
            history
        )

        history = calculate_mqd_score(
            history
        )

        latest = history.iloc[-1]
        previous = history.iloc[-2]

        current_price = float(
            latest["Close"]
        )

        previous_price = float(
            previous["Close"]
        )

        change_pct = (
            (
                current_price
                - previous_price
            )
            / previous_price
        ) * 100

        rsi = float(
            latest["RSI"]
        )

        mqd_score = float(
            latest["MQD Score"]
        )

        confidence = float(
            latest["Confidence Score"]
        )

        score_color = get_score_color(
            mqd_score
        )

        score_label = get_score_label(
            mqd_score
        )

        # -------------------------------------
        # Score
        # -------------------------------------

        st.markdown(
            f"""
            <h2 style="color:{score_color};">
            {asset.name}
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <h3 style="color:{score_color};">
            MQD Score : {mqd_score:.0f}
            ({score_label})
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # -------------------------------------
        # Metrics
        # -------------------------------------

        col1, col2 = st.columns(2)

        col3, col4 = st.columns(2)

        with col1:

            st.metric(
                "Current Price",
                f"{current_price:,.2f}",
            )

        with col2:

            st.metric(
                "Daily Change",
                f"{change_pct:.2f}%",
            )

        with col3:

            st.metric(
                "RSI",
                f"{rsi:.1f}",
            )

        with col4:

            st.metric(
                "MQD Score",
                f"{mqd_score:.0f}",
            )

        st.metric(
            "Confidence Score",
            f"{confidence:.0f}",
        )

        st.divider()

        # -------------------------------------
        # Price Chart
        # -------------------------------------

        draw_price_chart(history)

        st.divider()

        # -------------------------------------
        # Latest Data
        # -------------------------------------

        st.subheader("Latest Data")

        display_columns = [
            column
            for column in [
                "Close",
                "MA20",
                "MA60",
                "MA120",
                "RSI",
                "Momentum",
                "ROC",
                "MQD Score",
                "Confidence Score",
            ]
            if column in history.columns
        ]

        st.dataframe(
            history[display_columns].tail(30),
            use_container_width=True,
        )

        st.divider()

        # -------------------------------------
        # Last Update
        # -------------------------------------

        st.caption(
            f"Last Update : {get_last_update()}"
        )

        st.caption(
            "MQD Dashboard v1.0"
        )

    except Exception as exc:

        logger.exception(
            "Dashboard execution failed."
        )

        st.error(
            "데이터 처리 중 오류가 발생했습니다."
        )

        with st.expander(
            "오류 상세",
            expanded=False,
        ):
            st.exception(exc)

else:

    st.info(
        """
        왼쪽 사이드바에서

        1. Market 선택

        2. 종목 선택

        3. Download Data 클릭

        하면 MQD 분석이 시작됩니다.
        """
    )
