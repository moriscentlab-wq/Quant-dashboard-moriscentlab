"""
Yahoo Finance Collector

MQD (Mori Quant Dashboard)

Supports

- Korea
- US
- ETF
- Index
- FX
- Commodity
- Crypto

Python 3.12
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st
import yfinance as yf

logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1d"


# ==========================================================
# Column Mapping
# ==========================================================

RENAME_MAP: dict[str, str] = {
    "Adj Close": "Adj_Close",
    "AdjClose": "Adj_Close",
    "Close*": "Close",
    "Volume*": "Volume",
}


# ==========================================================
# Internal Helpers
# ==========================================================


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert MultiIndex columns into normal columns.

    yfinance >=0.2 sometimes returns

    ('Close','AAPL')

    instead of

    Close
    """

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            col[0] if isinstance(col, tuple) else str(col)
            for col in df.columns
        ]

    return df


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Yahoo column names.
    """

    df = df.rename(columns=RENAME_MAP)

    return df


def _ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure datetime index.
    """

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    return df


def _sort_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort by date.
    """

    return df.sort_index()


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dataframe returned from yfinance.
    """

    if df.empty:
        return df

    df = _flatten_columns(df)

    df = _rename_columns(df)

    df = _ensure_datetime_index(df)

    df = _sort_dataframe(df)

    return df


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate required columns.
    """

    required = {
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    }

    missing = required - set(df.columns)

    if missing:
        logger.warning(
            "Missing Yahoo columns: %s",
            sorted(missing),
        )

    return df


def _safe_download(
    ticker: str,
    *,
    period: str,
    interval: str,
) -> pd.DataFrame:
    """
    Safe wrapper around yfinance.download().
    """

    try:
        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

        if df.empty:
            logger.warning("No data: %s", ticker)
            return pd.DataFrame()

        df = _normalize_dataframe(df)

        df = _validate_dataframe(df)

        return df

    except Exception:
        logger.exception(
            "Yahoo download failed: %s",
            ticker,
        )
        return pd.DataFrame()


# ==========================================================
# Streamlit Cache
# ==========================================================


@st.cache_data(show_spinner=False, ttl=900)
def _cached_download(
    ticker: str,
    period: str,
    interval: str,
) -> pd.DataFrame:
    """
    Cached Yahoo download.
    """

    return _safe_download(
        ticker=ticker,
        period=period,
        interval=interval,
    )

# ==========================================================
# Public APIs
# ==========================================================


@st.cache_data(show_spinner=False, ttl=900)
def get_history(
    ticker: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> pd.DataFrame:
    """
    Get historical OHLCV data.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker.

    period : str
        ex)
        1mo
        3mo
        6mo
        1y
        2y
        5y
        max

    interval : str
        ex)
        1d
        1wk
        1mo

    Returns
    -------
    pd.DataFrame
    """

    ticker = ticker.strip().upper()

    if not ticker:
        logger.warning("Ticker is empty.")
        return pd.DataFrame()

    return _cached_download(
        ticker=ticker,
        period=period,
        interval=interval,
    )


def get_latest_price(
    ticker: str,
) -> Optional[float]:
    """
    Return latest close price.
    """

    df = get_history(
        ticker=ticker,
        period="5d",
    )

    if df.empty:
        return None

    try:
        return float(df["Close"].iloc[-1])

    except Exception:
        logger.exception(
            "Latest price error : %s",
            ticker,
        )
        return None


def get_last_update(
    ticker: str,
) -> Optional[datetime]:
    """
    Return latest market datetime.
    """

    df = get_history(
        ticker=ticker,
        period="5d",
    )

    if df.empty:
        return None

    try:
        return df.index[-1].to_pydatetime()

    except Exception:
        logger.exception(
            "Last update error : %s",
            ticker,
        )
        return None


def get_daily_change(
    ticker: str,
) -> Optional[float]:
    """
    Daily percentage change.
    """

    df = get_history(
        ticker=ticker,
        period="5d",
    )

    if len(df) < 2:
        return None

    try:

        previous = float(df["Close"].iloc[-2])
        current = float(df["Close"].iloc[-1])

        if previous == 0:
            return None

        return (current - previous) / previous * 100

    except Exception:
        logger.exception(
            "Daily change failed : %s",
            ticker,
        )
        return None


def get_returns(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> pd.Series:
    """
    Daily return series.
    """

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if df.empty:
        return pd.Series(dtype=float)

    try:

        returns = df["Close"].pct_change()

        return returns.dropna()

    except Exception:

        logger.exception(
            "Return calculation failed : %s",
            ticker,
        )

        return pd.Series(dtype=float)


def get_change_percent(
    ticker: str,
    days: int = 20,
) -> Optional[float]:
    """
    Percentage return over N days.
    """

    if days < 1:
        return None

    period = "1y"

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if len(df) <= days:
        return None

    try:

        past = float(df["Close"].iloc[-days - 1])
        current = float(df["Close"].iloc[-1])

        if past == 0:
            return None

        return (current - past) / past * 100

    except Exception:

        logger.exception(
            "Change percent failed : %s",
            ticker,
        )

        return None


def get_volume(
    ticker: str,
) -> Optional[int]:
    """
    Latest trading volume.
    """

    df = get_history(
        ticker=ticker,
        period="5d",
    )

    if df.empty:
        return None

    try:
        return int(df["Volume"].iloc[-1])

    except Exception:

        logger.exception(
            "Volume error : %s",
            ticker,
        )

        return None


def get_market_cap(
    ticker: str,
) -> Optional[float]:
    """
    Market capitalization.
    """

    try:

        info = yf.Ticker(ticker).fast_info

        if not info:
            return None

        value = info.get("marketCap")

        if value is None:
            return None

        return float(value)

    except Exception:

        logger.exception(
            "Market cap error : %s",
            ticker,
        )

        return None

# ==========================================================
# Batch Download
# ==========================================================


def download_many(
    tickers: list[str],
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> dict[str, pd.DataFrame]:
    """
    Download multiple tickers individually.

    Returns
    -------
    dict[str, pd.DataFrame]
        {
            "AAPL": dataframe,
            "MSFT": dataframe,
        }
    """

    results: dict[str, pd.DataFrame] = {}

    for ticker in tickers:

        try:

            df = get_history(
                ticker=ticker,
                period=period,
                interval=interval,
            )

            if not df.empty:
                results[ticker] = df

        except Exception:

            logger.exception(
                "Failed downloading %s",
                ticker,
            )

    return results


# ==========================================================
# Latest Snapshot
# ==========================================================


def get_snapshot(
    ticker: str,
) -> dict[str, Optional[float]]:
    """
    Latest market snapshot.

    Returns
    -------
    {
        "price": ...,
        "change": ...,
        "volume": ...,
        "market_cap": ...
    }
    """

    return {
        "price": get_latest_price(ticker),
        "change": get_daily_change(ticker),
        "volume": get_volume(ticker),
        "market_cap": get_market_cap(ticker),
    }


def get_snapshots(
    tickers: list[str],
) -> pd.DataFrame:
    """
    Snapshot dataframe.

    Index
    -----
    ticker
    """

    rows: list[dict] = []

    for ticker in tickers:

        try:

            snap = get_snapshot(ticker)

            rows.append(
                {
                    "Ticker": ticker,
                    "Price": snap["price"],
                    "DailyChange": snap["change"],
                    "Volume": snap["volume"],
                    "MarketCap": snap["market_cap"],
                }
            )

        except Exception:

            logger.exception(
                "Snapshot failed : %s",
                ticker,
            )

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    df.set_index(
        "Ticker",
        inplace=True,
    )

    return df


# ==========================================================
# Utilities
# ==========================================================


def is_valid_ticker(
    ticker: str,
) -> bool:
    """
    Check whether Yahoo Finance returns data.
    """

    df = get_history(
        ticker=ticker,
        period="5d",
    )

    return not df.empty


def filter_valid_tickers(
    tickers: list[str],
) -> list[str]:
    """
    Remove unavailable tickers.
    """

    valid: list[str] = []

    for ticker in tickers:

        try:

            if is_valid_ticker(ticker):
                valid.append(ticker)

        except Exception:

            logger.exception(
                "Ticker validation failed : %s",
                ticker,
            )

    return valid


def get_close_series(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> pd.Series:
    """
    Return close price series.
    """

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if df.empty:
        return pd.Series(dtype=float)

    return df["Close"]


def get_volume_series(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> pd.Series:
    """
    Return volume series.
    """

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if df.empty:
        return pd.Series(dtype=float)

    return df["Volume"]


def get_high_low(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> tuple[Optional[float], Optional[float]]:
    """
    Highest and lowest prices within the period.
    """

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if df.empty:
        return None, None

    try:

        highest = float(df["High"].max())
        lowest = float(df["Low"].min())

        return highest, lowest

    except Exception:

        logger.exception(
            "High/Low calculation failed : %s",
            ticker,
        )

        return None, None


def get_price_range(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> Optional[float]:
    """
    Price range (High - Low) over the period.
    """

    high, low = get_high_low(
        ticker=ticker,
        period=period,
    )

    if high is None or low is None:
        return None

    return high - low

# ==========================================================
# Asset Summary
# ==========================================================


def get_asset_summary(
    ticker: str,
    period: str = DEFAULT_PERIOD,
) -> dict[str, Optional[float]]:
    """
    Return a summary of the specified asset.
    """

    df = get_history(
        ticker=ticker,
        period=period,
    )

    if df.empty:
        return {}

    try:
        latest_close = float(df["Close"].iloc[-1])
        latest_volume = int(df["Volume"].iloc[-1])

        previous_close = (
            float(df["Close"].iloc[-2])
            if len(df) >= 2
            else latest_close
        )

        daily_change = (
            (latest_close - previous_close)
            / previous_close
            * 100
            if previous_close != 0
            else None
        )

        high = float(df["High"].max())
        low = float(df["Low"].min())

        return {
            "Ticker": ticker,
            "Close": latest_close,
            "DailyChange": daily_change,
            "High": high,
            "Low": low,
            "Range": high - low,
            "Volume": latest_volume,
            "MarketCap": get_market_cap(ticker),
            "LastUpdate": get_last_update(ticker),
        }

    except Exception:

        logger.exception(
            "Asset summary failed : %s",
            ticker,
        )

        return {}


def get_assets_summary(
    tickers: list[str],
    period: str = DEFAULT_PERIOD,
) -> pd.DataFrame:
    """
    Summary DataFrame for multiple assets.
    """

    rows: list[dict] = []

    for ticker in tickers:

        summary = get_asset_summary(
            ticker=ticker,
            period=period,
        )

        if summary:
            rows.append(summary)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    if "Ticker" in df.columns:
        df.set_index("Ticker", inplace=True)

    return df


# ==========================================================
# Export
# ==========================================================

__all__ = [
    "download_many",
    "filter_valid_tickers",
    "get_asset_summary",
    "get_assets_summary",
    "get_change_percent",
    "get_close_series",
    "get_daily_change",
    "get_high_low",
    "get_history",
    "get_last_update",
    "get_latest_price",
    "get_market_cap",
    "get_price_range",
    "get_returns",
    "get_snapshot",
    "get_snapshots",
    "get_volume",
    "get_volume_series",
    "is_valid_ticker",
]
