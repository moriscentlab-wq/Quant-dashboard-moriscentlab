"""
MQD Dashboard
Yahoo Finance Data Collector

Author : Mori Quant Dashboard
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
    Download historical price data from Yahoo Finance.

    Parameters
    ----------
    ticker : str
        Yahoo ticker symbol.
    period : str
        Download period.
    interval : str
        Candle interval.

    Returns
    -------
    pd.DataFrame
        Historical OHLCV DataFrame.

    Raises
    ------
    ConnectionError
        Yahoo download failed.
    ValueError
        Empty dataframe or invalid dataframe.
    """

    logger.info("Downloading Yahoo data : %s", ticker)

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
        logger.exception("Yahoo Finance connection failed.")
        raise ConnectionError(
            f"Failed to download data : {ticker}"
        ) from exc

    if df.empty:
        logger.error("Empty dataframe : %s", ticker)
        raise ValueError(
            f"No data returned for {ticker}"
        )

    # -----------------------------------
    # MultiIndex 처리
    # -----------------------------------

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # -----------------------------------
    # Adj Close 제거
    # -----------------------------------

    if "Adj Close" in df.columns:
        df = df.drop(columns="Adj Close")

    # -----------------------------------
    # 컬럼명 표준화
    # -----------------------------------

    rename_map = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }

    df.rename(columns=rename_map, inplace=True)

    # -----------------------------------
    # 필수 컬럼 확인
    # -----------------------------------

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns : {missing}"
        )

    df = df[REQUIRED_COLUMNS].copy()

    df.sort_index(inplace=True)

    logger.info(
        "%s downloaded successfully (%d rows)",
        ticker,
        len(df),
    )

    return df


def get_last_update() -> str:
    """
    Return current local datetime.

    Returns
    -------
    str
        YYYY-MM-DD HH:MM
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M")
