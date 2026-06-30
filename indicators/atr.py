"""
Average True Range (ATR)

MQD v2 Risk Engine

Purpose
-------
- Measure market volatility
- Support risk estimation
- Support stop-loss logic

This module DOES NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOW = 14


# ==========================================================
# Validation
# ==========================================================


def _validate_dataframe(
    data: pd.DataFrame,
) -> None:
    """
    Validate OHLC DataFrame.
    """

    required = ["High", "Low", "Close"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


def _validate_window(
    window: int,
) -> None:
    """
    Validate ATR window.
    """

    if window <= 0:
        raise ValueError("Window must be > 0")


# ==========================================================
# True Range
# ==========================================================


def calculate_true_range(
    data: pd.DataFrame,
) -> pd.Series:
    """
    True Range calculation.
    """

    high = data["High"]
    low = data["Low"]
    close = data["Close"]

    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1,
    ).max(axis=1)

    return true_range


# ==========================================================
# ATR Calculation
# ==========================================================


def calculate_atr(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Calculate Average True Range (ATR).
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        tr = calculate_true_range(data)

        atr = tr.ewm(
            span=window,
            adjust=False,
        ).mean()

        return atr

    except Exception:

        logger.exception(
            "Failed calculating ATR."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_atr(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """
    Append ATR column.
    """

    df = data.copy()

    df["ATR"] = calculate_atr(df, window)

    return df

"""
Average True Range (ATR)

MQD v2 Risk Engine

Purpose
-------
- Measure market volatility
- Support risk estimation
- Support stop-loss logic

This module DOES NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOW = 14


# ==========================================================
# Validation
# ==========================================================


def _validate_dataframe(
    data: pd.DataFrame,
) -> None:
    """
    Validate OHLC DataFrame.
    """

    required = ["High", "Low", "Close"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


def _validate_window(
    window: int,
) -> None:
    """
    Validate ATR window.
    """

    if window <= 0:
        raise ValueError("Window must be > 0")


# ==========================================================
# True Range
# ==========================================================


def calculate_true_range(
    data: pd.DataFrame,
) -> pd.Series:
    """
    True Range calculation.
    """

    high = data["High"]
    low = data["Low"]
    close = data["Close"]

    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1,
    ).max(axis=1)

    return true_range


# ==========================================================
# ATR Calculation
# ==========================================================


def calculate_atr(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Calculate Average True Range (ATR).
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        tr = calculate_true_range(data)

        atr = tr.ewm(
            span=window,
            adjust=False,
        ).mean()

        return atr

    except Exception:

        logger.exception(
            "Failed calculating ATR."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_atr(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """
    Append ATR column.
    """

    df = data.copy()

    df["ATR"] = calculate_atr(df, window)

    return df
