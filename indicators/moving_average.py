"""
Moving Average Indicators

MQD v2

Supported
---------
- SMA
- EMA
- Trend
- Golden Cross
- Dead Cross
- Moving Average Slope

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ==========================================================
# Validation
# ==========================================================


def _validate_dataframe(
    data: pd.DataFrame,
) -> None:
    """
    Validate OHLC dataframe.
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        raise KeyError("Close column not found.")


def _validate_window(
    window: int,
) -> None:
    """
    Validate moving average window.
    """

    if window <= 0:
        raise ValueError(
            "Window must be greater than zero."
        )


# ==========================================================
# Simple Moving Average
# ==========================================================


def calculate_sma(
    data: pd.DataFrame,
    window: int = 20,
) -> pd.Series:
    """
    Calculate Simple Moving Average.

    Parameters
    ----------
    data
        OHLC dataframe.

    window
        Rolling window.

    Returns
    -------
    pd.Series
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        return (
            data["Close"]
            .rolling(window=window)
            .mean()
        )

    except Exception:

        logger.exception(
            "Failed calculating SMA."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# Exponential Moving Average
# ==========================================================


def calculate_ema(
    data: pd.DataFrame,
    window: int = 20,
) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        return (
            data["Close"]
            .ewm(
                span=window,
                adjust=False,
            )
            .mean()
        )

    except Exception:

        logger.exception(
            "Failed calculating EMA."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# Add Moving Averages
# ==========================================================


def add_sma(
    data: pd.DataFrame,
    windows: list[int] | None = None,
) -> pd.DataFrame:
    """
    Append SMA columns.
    """

    if windows is None:

        windows = [
            5,
            10,
            20,
            60,
            120,
            200,
        ]

    df = data.copy()

    for window in windows:

        df[f"SMA_{window}"] = calculate_sma(
            df,
            window,
        )

    return df


def add_ema(
    data: pd.DataFrame,
    windows: list[int] | None = None,
) -> pd.DataFrame:
    """
    Append EMA columns.
    """

    if windows is None:

        windows = [
            5,
            10,
            20,
            60,
            120,
            200,
        ]

    df = data.copy()

    for window in windows:

        df[f"EMA_{window}"] = calculate_ema(
            df,
            window,
        )

    return df

# ==========================================================
# Moving Average Slope
# ==========================================================


def calculate_ma_slope(
    ma: pd.Series,
    periods: int = 5,
) -> pd.Series:
    """
    Calculate moving average slope.

    Positive
        Uptrend

    Negative
        Downtrend
    """

    if ma.empty:
        return pd.Series(dtype=float)

    return ma.diff(periods)


def calculate_ma_slope_percent(
    ma: pd.Series,
    periods: int = 5,
) -> pd.Series:
    """
    Percentage slope.
    """

    if ma.empty:
        return pd.Series(dtype=float)

    previous = ma.shift(periods)

    slope = (
        (ma - previous)
        / previous.replace(0, np.nan)
    ) * 100

    return slope


# ==========================================================
# Cross Detection
# ==========================================================


def is_golden_cross(
    fast_ma: pd.Series,
    slow_ma: pd.Series,
) -> bool:
    """
    Golden Cross

    fast crosses above slow.
    """

    if len(fast_ma) < 2:
        return False

    if len(slow_ma) < 2:
        return False

    return (
        fast_ma.iloc[-2] <= slow_ma.iloc[-2]
        and fast_ma.iloc[-1] > slow_ma.iloc[-1]
    )


def is_dead_cross(
    fast_ma: pd.Series,
    slow_ma: pd.Series,
) -> bool:
    """
    Dead Cross

    fast crosses below slow.
    """

    if len(fast_ma) < 2:
        return False

    if len(slow_ma) < 2:
        return False

    return (
        fast_ma.iloc[-2] >= slow_ma.iloc[-2]
        and fast_ma.iloc[-1] < slow_ma.iloc[-1]
    )


# ==========================================================
# Alignment
# ==========================================================


def is_bullish_alignment(
    data: pd.DataFrame,
) -> bool:
    """
    Bullish Alignment

    SMA20 > SMA60 > SMA120
    """

    required = [
        "SMA_20",
        "SMA_60",
        "SMA_120",
    ]

    if not all(
        column in data.columns
        for column in required
    ):
        return False

    latest = data.iloc[-1]

    return (
        latest["SMA_20"]
        > latest["SMA_60"]
        > latest["SMA_120"]
    )


def is_bearish_alignment(
    data: pd.DataFrame,
) -> bool:
    """
    Bearish Alignment

    SMA20 < SMA60 < SMA120
    """

    required = [
        "SMA_20",
        "SMA_60",
        "SMA_120",
    ]

    if not all(
        column in data.columns
        for column in required
    ):
        return False

    latest = data.iloc[-1]

    return (
        latest["SMA_20"]
        < latest["SMA_60"]
        < latest["SMA_120"]
    )


# ==========================================================
# Trend
# ==========================================================


def is_price_above_ma(
    data: pd.DataFrame,
    window: int = 20,
) -> bool:
    """
    Check whether the latest closing price
    is above the specified SMA.
    """

    column = f"SMA_{window}"

    if column not in data.columns:
        return False

    latest = data.iloc[-1]

    return latest["Close"] > latest[column]


def is_price_below_ma(
    data: pd.DataFrame,
    window: int = 20,
) -> bool:
    """
    Check whether the latest closing price
    is below the specified SMA.
    """

    column = f"SMA_{window}"

    if column not in data.columns:
        return False

    latest = data.iloc[-1]

    return latest["Close"] < latest[column]


def calculate_ma_distance(
    data: pd.DataFrame,
    window: int = 20,
) -> float:
    """
    Distance between Close and SMA (%).
    """

    column = f"SMA_{window}"

    if column not in data.columns:
        return np.nan

    latest = data.iloc[-1]

    ma = latest[column]

    if ma == 0:
        return np.nan

    return (
        (latest["Close"] - ma)
        / ma
        * 100
    )

# ==========================================================
# Trend Strength
# ==========================================================


def calculate_trend_strength(
    data: pd.DataFrame,
) -> float:
    """
    Calculate trend strength score.

    Returns
    -------
    float
        0 ~ 100
    """

    score = 0.0

    if is_price_above_ma(data, 20):
        score += 20

    if is_price_above_ma(data, 60):
        score += 20

    if is_price_above_ma(data, 120):
        score += 20

    if is_bullish_alignment(data):
        score += 40

    return score


# ==========================================================
# Alignment Score
# ==========================================================


def calculate_alignment_score(
    data: pd.DataFrame,
) -> float:
    """
    Alignment score.

    Bullish
        100

    Neutral
        50

    Bearish
        0
    """

    if is_bullish_alignment(data):
        return 100.0

    if is_bearish_alignment(data):
        return 0.0

    return 50.0


# ==========================================================
# Moving Average Score
# ==========================================================


def calculate_ma_score(
    data: pd.DataFrame,
) -> float:
    """
    MQD Moving Average score.

    Returns
    -------
    float
        0 ~ 100
    """

    trend = calculate_trend_strength(data)

    alignment = calculate_alignment_score(data)

    return (trend + alignment) / 2


# ==========================================================
# Trend Signal
# ==========================================================


def get_trend_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return trend signal.
    """

    score = calculate_ma_score(data)

    if score >= 80:
        return "Strong Bullish"

    if score >= 60:
        return "Bullish"

    if score >= 40:
        return "Neutral"

    if score >= 20:
        return "Bearish"

    return "Strong Bearish"


# ==========================================================
# Trend Columns
# ==========================================================


def add_trend_columns(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append trend-related columns.
    """

    df = data.copy()

    if "SMA_20" not in df.columns:
        df = add_sma(df)

    df["MA_Distance_20"] = (
        (df["Close"] - df["SMA_20"])
        / df["SMA_20"]
        * 100
    )

    df["MA_Distance_60"] = (
        (df["Close"] - df["SMA_60"])
        / df["SMA_60"]
        * 100
    )

    df["MA_Distance_120"] = (
        (df["Close"] - df["SMA_120"])
        / df["SMA_120"]
        * 100
    )

    df["BullishAlignment"] = (
        df["SMA_20"]
        > df["SMA_60"]
    ) & (
        df["SMA_60"]
        > df["SMA_120"]
    )

    df["BearishAlignment"] = (
        df["SMA_20"]
        < df["SMA_60"]
    ) & (
        df["SMA_60"]
        < df["SMA_120"]
    )

    return df


# ==========================================================
# Trend Summary
# ==========================================================


def get_ma_summary(
    data: pd.DataFrame,
) -> dict[str, float | str]:
    """
    Moving Average summary.
    """

    return {
        "trend_score": calculate_trend_strength(data),
        "alignment_score": calculate_alignment_score(data),
        "ma_score": calculate_ma_score(data),
        "signal": get_trend_signal(data),
    }

# ==========================================================
# Legacy Compatibility
# ==========================================================


def calculate_moving_average(
    data: pd.DataFrame,
    window: int = 20,
) -> pd.Series:
    """
    Backward-compatible wrapper.

    Existing MQD code imports:

        calculate_moving_average()

    This wrapper redirects to calculate_sma().
    """

    return calculate_sma(
        data=data,
        window=window,
    )


# ==========================================================
# Batch Calculation
# ==========================================================


def add_all_moving_averages(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add all supported moving averages
    and trend-related columns.
    """

    df = add_sma(data)

    df = add_ema(df)

    df = add_trend_columns(df)

    return df


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    # SMA / EMA
    "calculate_sma",
    "calculate_ema",
    "calculate_moving_average",
    "add_sma",
    "add_ema",
    "add_all_moving_averages",

    # Trend
    "calculate_ma_slope",
    "calculate_ma_slope_percent",
    "calculate_ma_distance",

    # Cross
    "is_golden_cross",
    "is_dead_cross",

    # Alignment
    "is_bullish_alignment",
    "is_bearish_alignment",

    # Price
    "is_price_above_ma",
    "is_price_below_ma",

    # MQD
    "calculate_trend_strength",
    "calculate_alignment_score",
    "calculate_ma_score",
    "get_trend_signal",
    "get_ma_summary",
]
