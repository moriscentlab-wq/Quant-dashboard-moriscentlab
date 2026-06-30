"""
MQD Dashboard
Price Chart Module
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def draw_price_chart(data: pd.DataFrame) -> None:
    """
    Draw price chart with moving averages.

    Parameters
    ----------
    data : pd.DataFrame
        Price dataframe.

    Returns
    -------
    None
    """

    if data.empty:
        st.warning("차트를 표시할 데이터가 없습니다.")
        return

    fig = go.Figure()

    # ---------------------------------------
    # Close
    # ---------------------------------------

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            name="Close",
            mode="lines",
            line=dict(
                width=3,
                color="#1f77b4",
            ),
        )
    )

    # ---------------------------------------
    # MA20
    # ---------------------------------------

    if "MA20" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA20"],
                name="MA20",
                mode="lines",
                line=dict(
                    width=1.5,
                    dash="solid",
                ),
            )
        )

    # ---------------------------------------
    # MA60
    # ---------------------------------------

    if "MA60" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA60"],
                name="MA60",
                mode="lines",
                line=dict(
                    width=1.5,
                    dash="dot",
                ),
            )
        )

    # ---------------------------------------
    # MA120
    # ---------------------------------------

    if "MA120" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA120"],
                name="MA120",
                mode="lines",
                line=dict(
                    width=1.5,
                    dash="dash",
                ),
            )
        )

    # ---------------------------------------
    # Layout
    # ---------------------------------------

    fig.update_layout(
        template="plotly_white",
        height=600,
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20,
        ),
        xaxis_title="Date",
        yaxis_title="Price",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
