"""
On-Balance Volume (OBV)

MQD v2 Indicator

Purpose
-------
- Measure cumulative buying/selling pressure
- Track volume-driven trend confirmation
- Support MQD Volume Engine

This module DOES NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_COLUMN = "Close"


# ==========================================================
# Validation
# ==========================================================


def _validate_dataframe(
    data: pd.DataFrame,
) -> None:
    """
    Validate OHLCV DataFrame.
    """

    required = ["Close", "Volume"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


# ==========================================================
# OBV Calculation
# ==========================================================


def calculate_obv(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Calculate On-Balance Volume (OBV).

    OBV logic:
    - If Close > previous Close → +Volume
    - If Close < previous Close → -Volume
    - Else → 0
    """

    _validate_dataframe(data)

    try:

        close = data["Close"]
        volume = data["Volume"]

        direction = close.diff()

        obv = np.where(
            direction > 0,
            volume,
            np.where(
                direction < 0,
                -volume,
                0,
            ),
        )

        return pd.Series(
            obv,
            index=data.index,
        ).cumsum()

    except Exception:

        logger.exception(
            "Failed calculating OBV."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_obv(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append OBV column.
    """

    df = data.copy()

    df["OBV"] = calculate_obv(df)

    return df

# ==========================================================
# OBV Slope / Momentum
# ==========================================================


def calculate_obv_slope(
    data: pd.DataFrame,
    periods: int = 5,
) -> float:
    """
    OBV slope over N periods.

    Positive → accumulation
    Negative → distribution
    """

    if "OBV" not in data.columns:
        data = add_obv(data)

    obv = data["OBV"]

    if len(obv) <= periods:
        return 0.0

    return float(obv.iloc[-1] - obv.iloc[-1 - periods])


# ==========================================================
# OBV State
# ==========================================================


def is_obv_rising(
    data: pd.DataFrame,
) -> bool:
    """
    OBV upward trend
    """

    return calculate_obv_slope(data) > 0


def is_obv_falling(
    data: pd.DataFrame,
) -> bool:
    """
    OBV downward trend
    """

    return calculate_obv_slope(data) < 0


# ==========================================================
# OBV Breakout Logic
# ==========================================================


def is_obv_breakout(
    data: pd.DataFrame,
    lookback: int = 20,
) -> bool:
    """
    Detect OBV breakout above recent range.
    """

    if "OBV" not in data.columns:
        data = add_obv(data)

    obv = data["OBV"]

    if len(obv) < lookback:
        return False

    recent = obv.iloc[-lookback:]

    return obv.iloc[-1] == recent.max()


# ==========================================================
# Signal Engine
# ==========================================================


def get_obv_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return OBV market signal.
    """

    if is_obv_breakout(data):
        return "Accumulation Breakout"

    if is_obv_rising(data):
        return "Accumulation"

    if is_obv_falling(data):
        return "Distribution"

    return "Neutral"


# ==========================================================
# Feature Engineering
# ==========================================================


def add_obv_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add OBV features for pipeline/scoring.
    """

    df = data.copy()

    if "OBV" not in df.columns:
        df = add_obv(df)

    df["OBV_Slope"] = df["OBV"].diff(5)

    df["OBV_Rising"] = df["OBV_Slope"] > 0

    df["OBV_Falling"] = df["OBV_Slope"] < 0

    df["OBV_Breakout"] = df["OBV"] == df["OBV"].rolling(20).max()

    return df


# ==========================================================
# Summary
# ==========================================================


def get_obv_summary(
    data: pd.DataFrame,
) -> dict[str, float | str | bool]:
    """
    OBV summary for MQD pipeline.
    """

    if "OBV" not in data.columns:
        data = add_obv(data)

    latest = data.iloc[-1]

    return {
        "obv": float(latest["OBV"]),
        "slope": calculate_obv_slope(data),
        "signal": get_obv_signal(data),
        "rising": is_obv_rising(data),
        "falling": is_obv_falling(data),
        "breakout": is_obv_breakout(data),
    }


# ==========================================================
# Public API
# ==========================================================


__all__ = [
    # Core
    "calculate_obv",
    "add_obv",

    # State
    "calculate_obv_slope",
    "is_obv_rising",
    "is_obv_falling",
    "is_obv_breakout",
    "get_obv_signal",

    # Features
    "add_obv_features",

    # Summary
    "get_obv_summary",
]
