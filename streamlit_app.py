import streamlit as st

from config.tickers import ALL_ASSETS
from collectors.yahoo import (
    get_latest_price,
    get_last_update,
)

st.set_page_config(
    page_title="MQD Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 MQD Dashboard")

st.caption("Moris Quant Dashboard")

st.divider()

st.subheader("🌍 Global Market")

results = []

for category, assets in ALL_ASSETS.items():

    with st.expander(category, expanded=False):

        for _, asset in assets.items():

            try:

                data = get_latest_price(asset.ticker)

                st.metric(
                    label=asset.name,
                    value=f"{data['close']:.2f}",
                    delta=f"{data['change_pct']:.2f}%"
                )

            except Exception as e:

                st.warning(
                    f"{asset.name}: {e}"
                )

st.divider()

st.caption(
    f"Last Update : {get_last_update()}"
)