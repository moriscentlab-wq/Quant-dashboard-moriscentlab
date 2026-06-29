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

                history = calculate_moving_average(history)
                history = calculate_rsi(history)
                history = calculate_mqd_score(history)

                latest = history.iloc[-1]
                previous = history.iloc[-2]
ranking.append(
    {
        "Market": category,
        "Name": asset.name,
        "Ticker": asset.ticker,
        "Price": round(float(latest["Close"]), 2),
        "RSI": round(float(latest["RSI"]), 1),
        "MQD": round(float(latest["MQD Score"]), 1),
    }
)

                
                close = float(latest["Close"])

                change_pct = (
                    (latest["Close"] - previous["Close"])
                    / previous["Close"]
                ) * 100

                st.metric(
                    label=f"{asset.name} | MQD {int(latest['MQD Score'])}",
                    value=f"{close:.2f}",
                    delta=f"{change_pct:.2f}%"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.caption(
                        f"RSI : {latest['RSI']:.1f}"
                    )

                with col2:
                    st.caption(
                        f"Confidence : {int(latest['Confidence Score'])}"
                    )

            except Exception as e:

                st.warning(
                    f"{asset.name}: {e}"
                )

st.divider()

st.caption(
    f"Last Update : {get_last_update()}"
)
st.divider()

st.subheader("🏆 MQD Ranking")

if ranking:

    df = pd.DataFrame(ranking)

    df = df.sort_values(
        by="MQD",
        ascending=False,
    ).reset_index(drop=True)

    df.index = df.index + 1

    st.dataframe(
        df,
        use_container_width=True,
    )

st.caption(
    f"Last Update : {get_last_update()}"
)
