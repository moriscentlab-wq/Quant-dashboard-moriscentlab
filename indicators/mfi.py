"""
Money Flow Index (MFI)

MQD v2 Indicator

Purpose
-------
- Measure buying/selling pressure
- Combine price + volume
- Detect money flow strength

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
    Validate OHLCV DataFrame.
    """

    required = ["High", "Low", "Close", "Volume"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


def _validate_window(
    window: int,
) -> None:
    """
    Validate MFI window.
    """

    if window <= 0:
        raise ValueError("Window must be > 0")


# ==========================================================
# Typical Price
# ==========================================================


def calculate_typical_price(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Typical Price = (High + Low + Close) / 3
    """

    return (
        data["High"]
        + data["Low"]
        + data["Close"]
    ) / 3


# ==========================================================
# Raw Money Flow
# ==========================================================


def calculate_raw_money_flow(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Raw Money Flow = Typical Price * Volume
    """

    tp = calculate_typical_price(data)

    return tp * data["Volume"]


# ==========================================================
# MFI Core (skeleton only)
# ==========================================================


def calculate_mfi(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Placeholder for MFI calculation (Part 2).
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:
        # To be implemented in Part 2
        return pd.Series(
            50.0,
            index=data.index,
        )

    except Exception:

        logger.exception(
            "Failed calculating MFI."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_mfi(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """
    Append MFI column.
    """

    df = data.copy()

    df["MFI"] = calculate_mfi(df, window)

    return df

# ==========================================================
# Money Flow Calculation
# ==========================================================


def calculate_positive_negative_money_flow(
    data: pd.DataFrame,
) -> tuple[pd.Series, pd.Series]:
    """
    Positive and Negative Money Flow
    """

    typical_price = calculate_typical_price(data)
    raw_flow = typical_price * data["Volume"]

    price_diff = typical_price.diff()

    positive_flow = raw_flow.where(price_diff > 0, 0.0)
    negative_flow = raw_flow.where(price_diff < 0, 0.0)

    return positive_flow, negative_flow


# ==========================================================
# MFI Core Calculation
# ==========================================================


def calculate_mfi(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Calculate Money Flow Index (MFI)
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        positive_flow, negative_flow = (
            calculate_positive_negative_money_flow(data)
        )

        mfi_values = []

        for i in range(len(data)):
            if i < window:
                mfi_values.append(50.0)
                continue

            pos_sum = positive_flow.iloc[i - window:i].sum()
            neg_sum = negative_flow.iloc[i - window:i].sum()

            if neg_sum == 0:
                mfi_values.append(100.0)
                continue

            money_flow_ratio = pos_sum / neg_sum

            mfi = 100 - (100 / (1 + money_flow_ratio))

            mfi_values.append(mfi)

        return pd.Series(
            mfi_values,
            index=data.index,
        )

    except Exception:

        logger.exception(
            "Failed calculating MFI."
        )

        return pd.Series(
            50.0,
            index=data.index,
        )


# ==========================================================
# Signal Engine
# ==========================================================


def is_mfi_overbought(
    data: pd.DataFrame,
    threshold: float = 80.0,
) -> bool:
    """
    MFI overbought condition
    """

    if "MFI" not in data.columns:
        data = add_mfi(data)

    return float(data["MFI"].iloc[-1]) >= threshold


def is_mfi_oversold(
    data: pd.DataFrame,
    threshold: float = 20.0,
) -> bool:
    """
    MFI oversold condition
    """

    if "MFI" not in data.columns:
        data = add_mfi(data)

    return float(data["MFI"].iloc[-1]) <= threshold


def is_mfi_bullish(
    data: pd.DataFrame,
) -> bool:
    """
    Bullish money flow (> 50)
    """

    if "MFI" not in data.columns:
        data = add_mfi(data)

    return float(data["MFI"].iloc[-1]) > 50


def is_mfi_bearish(
    data: pd.DataFrame,
) -> bool:
    """
    Bearish money flow (< 50)
    """

    if "MFI" not in data.columns:
        data = add_mfi(data)

    return float(data["MFI"].iloc[-1]) < 50


# ==========================================================
# Signal
# ==========================================================


def get_mfi_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return MFI market state
    """

    if is_mfi_overbought(data):
        return "Overbought"

    if is_mfi_oversold(data):
        return "Oversold"

    if is_mfi_bullish(data):
        return "Bullish Money Flow"

    return "Bearish Money Flow"

# ==========================================================
# Feature Engineering
# ==========================================================


def add_mfi_features(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """
    Add MFI-derived features.
    """

    df = data.copy()

    if "MFI" not in df.columns:
        df = add_mfi(df, window)

    df["MFI_Slope"] = df["MFI"].diff(3)

    df["MFI_Rising"] = df["MFI_Slope"] > 0
    df["MFI_Falling"] = df["MFI_Slope"] < 0

    df["MFI_Overbought"] = df["MFI"] >= 80
    df["MFI_Oversold"] = df["MFI"] <= 20

    df["MFI_Bullish"] = df["MFI"] > 50
    df["MFI_Bearish"] = df["MFI"] < 50

    return df


# ==========================================================
# Summary API
# ==========================================================


def get_mfi_summary(
    data: pd.DataFrame,
) -> dict[str, float | str | bool]:
    """
    Return MFI summary (no scoring logic).
    """

    if "MFI" not in data.columns:
        data = add_mfi(data)

    latest = data.iloc[-1]

    return {
        "mfi": float(latest["MFI"]),
        "signal": get_mfi_signal(data),
        "bullish": is_mfi_bullish(data),
        "bearish": is_mfi_bearish(data),
        "overbought": is_mfi_overbought(data),
        "oversold": is_mfi_oversold(data),
        "slope": float(df := data["MFI"].diff(3).iloc[-1]),
    }


# ==========================================================
# Legacy Compatibility
# ==========================================================


def calculate_mfi_indicator(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.Series:
    """
    Backward-compatible wrapper.
    """

    return calculate_mfi(data, window)


# ==========================================================
# Public Exports
# ==========================================================


__all__ = [
    # Core
    "calculate_mfi",
    "calculate_mfi_indicator",
    "calculate_typical_price",
    "calculate_raw_money_flow",

    # DataFrame
    "add_mfi",
    "add_mfi_features",

    # Signal
    "is_mfi_overbought",
    "is_mfi_oversold",
    "is_mfi_bullish",
    "is_mfi_bearish",
    "get_mfi_signal",

    # Summary
    "get_mfi_summary",
]
