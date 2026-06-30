"""
Moving Average Convergence Divergence (MACD)

MQD v2 Indicator

Responsibilities
----------------
- Calculate MACD
- Calculate Signal Line
- Calculate Histogram
- Append MACD columns

This module DOES NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_FAST = 12
DEFAULT_SLOW = 26
DEFAULT_SIGNAL = 9
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


def _validate_periods(
    fast: int,
    slow: int,
    signal: int,
) -> None:
    """
    Validate MACD parameters.
    """

    if fast <= 0:
        raise ValueError("fast must be > 0")

    if slow <= 0:
        raise ValueError("slow must be > 0")

    if signal <= 0:
        raise ValueError("signal must be > 0")

    if fast >= slow:
        raise ValueError(
            "fast period must be smaller than slow period."
        )


# ==========================================================
# MACD Calculation
# ==========================================================


def calculate_macd(
    data: pd.DataFrame,
    fast: int = DEFAULT_FAST,
    slow: int = DEFAULT_SLOW,
    signal: int = DEFAULT_SIGNAL,
) -> pd.DataFrame:
    """
    Calculate MACD.

    Returns
    -------
    DataFrame

    Columns
    -------
    MACD
    MACD_Signal
    MACD_Histogram
    """

    _validate_dataframe(data)
    _validate_periods(
        fast,
        slow,
        signal,
    )

    try:

        close = data[DEFAULT_COLUMN]

        ema_fast = close.ewm(
            span=fast,
            adjust=False,
        ).mean()

        ema_slow = close.ewm(
            span=slow,
            adjust=False,
        ).mean()

        macd = ema_fast - ema_slow

        signal_line = macd.ewm(
            span=signal,
            adjust=False,
        ).mean()

        histogram = (
            macd
            - signal_line
        )

        return pd.DataFrame(
            {
                "MACD": macd,
                "MACD_Signal": signal_line,
                "MACD_Histogram": histogram,
            },
            index=data.index,
        )

    except Exception:

        logger.exception(
            "Failed calculating MACD."
        )

        return pd.DataFrame(
            index=data.index,
        )


# ==========================================================
# DataFrame Helpers
# ==========================================================


def add_macd(
    data: pd.DataFrame,
    fast: int = DEFAULT_FAST,
    slow: int = DEFAULT_SLOW,
    signal: int = DEFAULT_SIGNAL,
) -> pd.DataFrame:
    """
    Append MACD columns.
    """

    df = data.copy()

    macd = calculate_macd(
        df,
        fast=fast,
        slow=slow,
        signal=signal,
    )

    return df.join(macd)


def get_latest_macd(
    data: pd.DataFrame,
) -> tuple[float, float, float]:
    """
    Return latest
    (MACD, Signal, Histogram)
    """

    if "MACD" not in data.columns:

        data = add_macd(data)

    latest = data.iloc[-1]

    return (
        float(latest["MACD"]),
        float(latest["MACD_Signal"]),
        float(latest["MACD_Histogram"]),
    )

# ==========================================================
# MACD Helpers
# ==========================================================


def is_histogram_positive(
    data: pd.DataFrame,
) -> bool:
    """
    Histogram > 0
    """

    if "MACD_Histogram" not in data.columns:
        data = add_macd(data)

    return float(data["MACD_Histogram"].iloc[-1]) > 0


def is_histogram_negative(
    data: pd.DataFrame,
) -> bool:
    """
    Histogram < 0
    """

    if "MACD_Histogram" not in data.columns:
        data = add_macd(data)

    return float(data["MACD_Histogram"].iloc[-1]) < 0


# ==========================================================
# MACD Trend State
# ==========================================================


def is_macd_bullish(
    data: pd.DataFrame,
) -> bool:
    """
    MACD line above Signal line
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    latest = data.iloc[-1]

    return latest["MACD"] > latest["MACD_Signal"]


def is_macd_bearish(
    data: pd.DataFrame,
) -> bool:
    """
    MACD line below Signal line
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    latest = data.iloc[-1]

    return latest["MACD"] < latest["MACD_Signal"]


# ==========================================================
# Cross Detection
# ==========================================================


def is_golden_cross(
    data: pd.DataFrame,
) -> bool:
    """
    MACD Golden Cross
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    if len(data) < 2:
        return False

    prev = data.iloc[-2]
    curr = data.iloc[-1]

    return (
        prev["MACD"] <= prev["MACD_Signal"]
        and curr["MACD"] > curr["MACD_Signal"]
    )


def is_dead_cross(
    data: pd.DataFrame,
) -> bool:
    """
    MACD Dead Cross
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    if len(data) < 2:
        return False

    prev = data.iloc[-2]
    curr = data.iloc[-1]

    return (
        prev["MACD"] >= prev["MACD_Signal"]
        and curr["MACD"] < curr["MACD_Signal"]
    )


# ==========================================================
# MACD Slope
# ==========================================================


def calculate_macd_slope(
    data: pd.DataFrame,
    periods: int = 3,
) -> float:
    """
    MACD momentum slope
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    macd = data["MACD"]

    if len(macd) <= periods:
        return 0.0

    return float(
        macd.iloc[-1] - macd.iloc[-1 - periods]
    )


# ==========================================================
# MACD Signal
# ==========================================================


def get_macd_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return MACD signal state
    """

    if is_golden_cross(data):
        return "Bullish Cross"

    if is_dead_cross(data):
        return "Bearish Cross"

    if is_macd_bullish(data) and is_histogram_positive(data):
        return "Bullish Momentum"

    if is_macd_bearish(data) and is_histogram_negative(data):
        return "Bearish Momentum"

    if is_macd_bullish(data):
        return "Bullish"

    if is_macd_bearish(data):
        return "Bearish"

    return "Neutral"

# ==========================================================
# Feature Engineering
# ==========================================================


def add_macd_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append MACD feature columns for pipeline/scoring use.
    """

    df = data.copy()

    if "MACD" not in df.columns:
        df = add_macd(df)

    df["MACD_Slope"] = calculate_macd_slope(df)

    df["MACD_Bullish"] = df["MACD"] > df["MACD_Signal"]

    df["MACD_Bearish"] = df["MACD"] < df["MACD_Signal"]

    df["MACD_Hist_Positive"] = df["MACD_Histogram"] > 0

    df["MACD_Hist_Negative"] = df["MACD_Histogram"] < 0

    df["MACD_Zero_Cross_Up"] = (
        (df["MACD"].shift(1) <= df["MACD_Signal"].shift(1))
        & (df["MACD"] > df["MACD_Signal"])
    )

    df["MACD_Zero_Cross_Down"] = (
        (df["MACD"].shift(1) >= df["MACD_Signal"].shift(1))
        & (df["MACD"] < df["MACD_Signal"])
    )

    return df


# ==========================================================
# Summary
# ==========================================================


def get_macd_summary(
    data: pd.DataFrame,
) -> dict[str, float | str | bool]:
    """
    Return MACD summary (no scoring logic).
    """

    if "MACD" not in data.columns:
        data = add_macd(data)

    macd, signal, hist = get_latest_macd(data)

    return {
        "macd": macd,
        "signal_line": signal,
        "histogram": hist,
        "state": get_macd_signal(data),
        "bullish": is_macd_bullish(data),
        "bearish": is_macd_bearish(data),
        "hist_positive": is_histogram_positive(data),
        "hist_negative": is_histogram_negative(data),
        "slope": calculate_macd_slope(data),
    }


# ==========================================================
# Legacy Compatibility
# ==========================================================


def calculate_macd_indicator(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Backward-compatible wrapper for old MQD code.
    """

    return calculate_macd(data)


# ==========================================================
# Public Exports
# ==========================================================


__all__ = [
    # Core
    "calculate_macd",
    "add_macd",
    "get_latest_macd",
    "calculate_macd_indicator",

    # Signals
    "is_macd_bullish",
    "is_macd_bearish",
    "is_golden_cross",
    "is_dead_cross",
    "is_histogram_positive",
    "is_histogram_negative",
    "get_macd_signal",

    # Features
    "calculate_macd_slope",
    "add_macd_features",

    # Summary
    "get_macd_summary",
]
