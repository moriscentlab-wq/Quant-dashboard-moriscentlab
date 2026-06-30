"""
MQD Dashboard
Price Chart
"""

from __future__ import annotations

import logging

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

logger = logging.getLogger(__name__)

PRICE_COLUMNS = [
    "Close",
    "MA20",
    "MA60",
    "MA120",
]


def draw_price_chart(
    data: pd.DataFrame,
) -> None:
    """
    Draw price chart using Plotly.

    Parameters
    ----------
    data : pd.DataFrame
        Price DataFrame.

    Returns
    -------
    None
    """

    logger.info("Drawing price chart")

    if data.empty:
        st.warning("No chart data available.")
        return

    if "Close" not in data.columns:
        st.warning("Close column not found.")
        return

    try:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close",
            )
        )

        for column in ["MA20", "MA60", "MA120"]:

            if column in data.columns:

                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[column],
                        mode="lines",
                        name=column,
                    )
                )

        fig.update_layout(

            title="Price Chart",

            template="plotly_white",

            height=600,

            hovermode="x unified",

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20,
            ),
        )

        fig.update_xaxes(
            showgrid=True,
        )

        fig.update_yaxes(
            showgrid=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        logger.info(
            "Price chart created successfully"
        )

    except Exception:

        logger.exception(
            "Failed to draw price chart."
        )

        st.error(
            "차트를 생성하는 중 오류가 발생했습니다."
        )
