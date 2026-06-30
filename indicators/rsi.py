"""
Relative Strength Index (RSI)

MQD v2 Indicator

Responsibilities
----------------
- Calculate RSI
- Append RSI column
- Generate RSI signals

This module DOES NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOW = 14
DEFAULT_COLUMN = "Close"


# ==========================================================
# Validation
# ==========================================================


def _validate_dataframe(
    data: pd.DataFrame,
) -> None:
    """
    Validate OHLC DataFrame.
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    if DEFAULT_COLUMN not in data.columns:
        raise KeyError(
            f"{DEFAULT_COLUMN} column not found."
        )


def _validate_window(
    window: int,
) -> None:
    """
    Validate RSI window.
    """

    if window <= 0:
        raise ValueError(
            "Window must be greater than zero."
        )


# ==========================================================
# RSI Calculation
# ==========================================================


def calculate_rsi(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).

    Parameters
    ----------
    data
        OHLC DataFrame.

    window
        RSI period.

    Returns
    -------
    pd.Series
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        close = data[DEFAULT_COLUMN]

        delta = close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / window,
            adjust=False,
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / window,
            adjust=False,
        ).mean()

        rs = avg_gain / avg_loss.replace(
            0,
            np.nan,
        )

        rsi = 100 - (100 / (1 + rs))

        return rsi.fillna(50.0)

    except Exception:

        logger.exception(
            "Failed calculating RSI."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helpers
# ==========================================================


def add_rsi(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """
    Append RSI column.
    """

    df = data.copy()

    df["RSI"] = calculate_rsi(
        df,
        window=window,
    )

    return df


def add_multiple_rsi(
    data: pd.DataFrame,
    windows: list[int],
) -> pd.DataFrame:
    """
    Append multiple RSI columns.

    Example
    -------
    RSI_7
    RSI_14
    RSI_21
    """

    df = data.copy()

    for window in windows:

        df[f"RSI_{window}"] = calculate_rsi(
            df,
            window=window,
        )

    return df

# ==========================================================
# RSI Thresholds
# ==========================================================

DEFAULT_OVERSOLD = 30.0
DEFAULT_OVERBOUGHT = 70.0
DEFAULT_NEUTRAL_LOW = 45.0
DEFAULT_NEUTRAL_HIGH = 55.0


# ==========================================================
# RSI States
# ==========================================================


def get_latest_rsi(
    data: pd.DataFrame,
) -> float:
    """
    Return latest RSI value.
    """

    if "RSI" not in data.columns:
        data = add_rsi(data)

    return float(data["RSI"].iloc[-1])


def is_overbought(
    data: pd.DataFrame,
    threshold: float = DEFAULT_OVERBOUGHT,
) -> bool:
    """
    RSI >= threshold
    """

    return get_latest_rsi(data) >= threshold


def is_oversold(
    data: pd.DataFrame,
    threshold: float = DEFAULT_OVERSOLD,
) -> bool:
    """
    RSI <= threshold
    """

    return get_latest_rsi(data) <= threshold


def is_neutral(
    data: pd.DataFrame,
) -> bool:
    """
    RSI in neutral zone.
    """

    rsi = get_latest_rsi(data)

    return (
        DEFAULT_NEUTRAL_LOW
        <= rsi
        <= DEFAULT_NEUTRAL_HIGH
    )


def is_rsi_bullish(
    data: pd.DataFrame,
) -> bool:
    """
    RSI above 50.
    """

    return get_latest_rsi(data) >= 50.0


def is_rsi_bearish(
    data: pd.DataFrame,
) -> bool:
    """
    RSI below 50.
    """

    return get_latest_rsi(data) < 50.0


# ==========================================================
# RSI Slope
# ==========================================================


def calculate_rsi_slope(
    data: pd.DataFrame,
    periods: int = 3,
) -> float:
    """
    RSI slope over N periods.
    """

    if "RSI" not in data.columns:
        data = add_rsi(data)

    rsi = data["RSI"]

    if len(rsi) <= periods:
        return 0.0

    return float(
        rsi.iloc[-1]
        - rsi.iloc[-1 - periods]
    )


def is_rsi_rising(
    data: pd.DataFrame,
) -> bool:
    """
    True if RSI slope is positive.
    """

    return calculate_rsi_slope(data) > 0


def is_rsi_falling(
    data: pd.DataFrame,
) -> bool:
    """
    True if RSI slope is negative.
    """

    return calculate_rsi_slope(data) < 0


# ==========================================================
# RSI Signal
# ==========================================================


def get_rsi_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return RSI signal.
    """

    if is_overbought(data):
        return "Overbought"

    if is_oversold(data):
        return "Oversold"

    if is_rsi_bullish(data):
        return "Bullish"

    return "Bearish"

# ==========================================================
# Feature Engineering
# ==========================================================


def add_rsi_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append RSI-derived feature columns.

    These features are intended for
    pipeline/scoring modules.
    """

    df = data.copy()

    if "RSI" not in df.columns:
        df = add_rsi(df)

    df["RSI_Slope"] = (
        df["RSI"]
        .diff(3)
    )

    df["RSI_Rising"] = (
        df["RSI_Slope"] > 0
    )

    df["RSI_Falling"] = (
        df["RSI_Slope"] < 0
    )

    df["RSI_Overbought"] = (
        df["RSI"] >= DEFAULT_OVERBOUGHT
    )

    df["RSI_Oversold"] = (
        df["RSI"] <= DEFAULT_OVERSOLD
    )

    df["RSI_Bullish"] = (
        df["RSI"] >= 50
    )

    df["RSI_Bearish"] = (
        df["RSI"] < 50
    )

    return df


# ==========================================================
# Relative Strength
# ==========================================================


def calculate_relative_strength(
    data: pd.DataFrame,
) -> float:
    """
    Normalized RSI value.

    Returns
    -------
    float

    0.0 ~ 1.0
    """

    rsi = get_latest_rsi(data)

    return max(
        0.0,
        min(
            1.0,
            rsi / 100.0,
        ),
    )


# ==========================================================
# Summary
# ==========================================================


def get_rsi_summary(
    data: pd.DataFrame,
) -> dict[str, float | bool | str]:
    """
    Return RSI summary.

    This function contains
    no scoring logic.
    """

    return {
        "rsi": get_latest_rsi(data),
        "signal": get_rsi_signal(data),
        "rising": is_rsi_rising(data),
        "falling": is_rsi_falling(data),
        "bullish": is_rsi_bullish(data),
        "bearish": is_rsi_bearish(data),
        "overbought": is_overbought(data),
        "oversold": is_oversold(data),
        "relative_strength": calculate_relative_strength(
            data
        ),
    }


# ==========================================================
# Legacy Compatibility
# ==========================================================


def calculate_rsi_indicator(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Backward-compatible wrapper.
    """

    return calculate_rsi(
        data=data,
        window=window,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    # Calculation
    "calculate_rsi",
    "calculate_rsi_indicator",

    # DataFrame
    "add_rsi",
    "add_multiple_rsi",
    "add_rsi_features",

    # States
    "get_latest_rsi",
    "is_overbought",
    "is_oversold",
    "is_neutral",
    "is_rsi_bullish",
    "is_rsi_bearish",

    # Trend
    "calculate_rsi_slope",
    "is_rsi_rising",
    "is_rsi_falling",

    # Signal
    "get_rsi_signal",

    # Summary
    "calculate_relative_strength",
    "get_rsi_summary",
]
