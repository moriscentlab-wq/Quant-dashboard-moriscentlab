"""
MQD Dashboard v1.0
Main Streamlit Application
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.tickers import ALL_ASSETS

from collectors.yahoo import (
    get_history,
    get_last_update,
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

from charts.price_chart import (
    draw_price_chart,
)

from utils.colors import (
    get_score_color,
    get_score_label,
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD Dashboard")
st.caption("Moris Quant Dashboard")

st.divider()

ranking: list[dict] = []

# -------------------------------------------------
# Global Market
# -------------------------------------------------

st.subheader("🌍 Global Market")

for category, assets in ALL_ASSETS.items():

    with st.expander(category, expanded=False):

        for asset in assets.values():

            try:

                # ---------------------------------
                # Download History
                # ---------------------------------

                history = get_history(asset.ticker)

                if history.empty:
                    st.warning(
                        f"{asset.name} 데이터를 불러올 수 없습니다."
                    )
                    continue

                # ---------------------------------
                # Indicators
                # ---------------------------------

                history = calculate_moving_average(
                    history
                )

                history = calculate_rsi(
                    history
                )

                history = calculate_mqd_score(
                    history
                )

                if len(history) < 2:
                    st.warning(
                        f"{asset.name} 데이터가 부족합니다."
                    )
                    continue

                latest = history.iloc[-1]
                previous = history.iloc[-2]

                # ---------------------------------
                # Latest Values
                # ---------------------------------

                current_price = float(latest["Close"])
                previous_price = float(previous["Close"])

                change_pct = (
                    (current_price - previous_price)
                    / previous_price
                ) * 100

                rsi = float(latest["RSI"])

                mqd_score = float(
                    latest["MQD Score"]
                )

                confidence = float(
                    latest["Confidence Score"]
                )

                # ---------------------------------
                # Ranking
                # ---------------------------------

                ranking.append(
                    {
                        "Market": category,
                        "Name": asset.name,
                        "Ticker": asset.ticker,
                        "Price": round(current_price, 2),
                        "Change (%)": round(change_pct, 2),
                        "RSI": round(rsi, 1),
                        "MQD": round(mqd_score, 1),
                    }
                )

                # ---------------------------------
                # Score Style
                # ---------------------------------

                score_color = get_score_color(
                    mqd_score
                )

                score_label = get_score_label(
                    mqd_score
                )

                # ---------------------------------
                # Title
                # ---------------------------------

                st.markdown(
                    f"## {asset.name}"
                )

                st.markdown(
                    f"""
                    <h3 style='color:{score_color};'>
                    MQD Score : {mqd_score:.0f}
                    ({score_label})
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                # ---------------------------------
                # Metrics
                # ---------------------------------

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "현재가",
                        f"{current_price:,.2f}",
                    )

                with col2:
                    st.metric(
                        "등락률",
                        f"{change_pct:.2f}%",
                    )

                with col3:
                    st.metric(
                        "RSI",
                        f"{rsi:.1f}",
                    )

                with col4:
                    st.metric(
                        "Confidence",
                        f"{confidence:.0f}",
                    )


                # ---------------------------------
                # Price Chart
                # ---------------------------------

                draw_price_chart(history)

                st.divider()

            except Exception as e:

                st.error(
                    f"{asset.name} 데이터를 처리하는 중 오류가 발생했습니다."
                )

                with st.expander("오류 상세", expanded=False):
                    st.exception(e)

# -------------------------------------------------
# MQD Ranking
# -------------------------------------------------

st.divider()

st.subheader("🏆 MQD Ranking")

if ranking:

    ranking_df = pd.DataFrame(ranking)

    ranking_df = ranking_df.sort_values(
        by="MQD",
        ascending=False,
    ).reset_index(drop=True)

    ranking_df.index += 1

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=False,
    )

else:

    st.info("표시할 MQD 데이터가 없습니다.")

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

try:

    st.caption(
        f"Last Update : {get_last_update()}"
    )

except Exception:

    st.caption("Last Update : -")

st.caption("MQD Dashboard v1.0")
