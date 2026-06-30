"""
MQD Dashboard
Yahoo Finance Data Collector
"""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd
import streamlit as st
import yfinance as yf

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


@st.cache_data(ttl=300, show_spinner=False)
def get_history(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download historical OHLCV data from Yahoo Finance.
    """

    logger.info("Downloading Yahoo Finance data: %s", ticker)

    try:

        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

    except Exception as exc:

        logger.exception("Yahoo Finance download failed.")

        raise ConnectionError(
            f"Failed to download data for {ticker}"
        ) from exc

    if df.empty:

        logger.error("Empty DataFrame returned.")

        raise ValueError(
            f"No data returned for {ticker}"
        )

    # -------------------------------------
    # Handle MultiIndex Columns
    # -------------------------------------

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = df.columns.get_level_values(0)

    # -------------------------------------
    # Remove Adj Close
    # -------------------------------------

    if "Adj Close" in df.columns:

        df = df.drop(columns=["Adj Close"])

    # -------------------------------------
    # Normalize column names
    # -------------------------------------

    rename_map = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }

    df.rename(columns=rename_map, inplace=True)

    # -------------------------------------
    # Validate required columns
    # -------------------------------------

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:

        logger.error("Missing columns: %s", missing)

        raise ValueError(
            f"Missing columns: {missing}"
        )

    df = df[REQUIRED_COLUMNS].copy()

    df.sort_index(inplace=True)

    logger.info(
        "Downloaded %d rows for %s",
        len(df),
        ticker,
    )

    return df


def get_last_update() -> str:
    """
    Return current local timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
