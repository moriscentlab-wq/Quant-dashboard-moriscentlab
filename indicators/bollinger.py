"""
Bollinger Bands Indicator

MQD v2

Purpose
-------
- Volatility measurement
- Breakout detection
- Mean reversion signal

This module does NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOW = 20
DEFAULT_STD = 2.0
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
    Validate window size.
    """

    if window <= 0:
        raise ValueError("Window must be > 0")


# ==========================================================
# Bollinger Bands Calculation
# ==========================================================


def calculate_bollinger_bands(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
    std: float = DEFAULT_STD,
) -> pd.DataFrame:
    """
    Calculate Bollinger Bands.

    Returns
    -------
    DataFrame
        middle, upper, lower bands
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        close = data[DEFAULT_COLUMN]

        ma = close.rolling(window=window).mean()

        std_dev = close.rolling(window=window).std()

        upper = ma + std * std_dev
        lower = ma - std * std_dev

        return pd.DataFrame(
            {
                "BB_Middle": ma,
                "BB_Upper": upper,
                "BB_Lower": lower,
            },
            index=data.index,
        )

    except Exception:

        logger.exception(
            "Failed calculating Bollinger Bands."
        )

        return pd.DataFrame(index=data.index)


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_bollinger(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
    std: float = DEFAULT_STD,
) -> pd.DataFrame:
    """
    Append Bollinger Bands columns.
    """

    df = data.copy()

    bands = calculate_bollinger_bands(
        df,
        window=window,
        std=std,
    )

    return df.join(bands)

"""
Bollinger Bands Indicator

MQD v2

Purpose
-------
- Volatility measurement
- Breakout detection
- Mean reversion signal

This module does NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOW = 20
DEFAULT_STD = 2.0
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
    Validate window size.
    """

    if window <= 0:
        raise ValueError("Window must be > 0")


# ==========================================================
# Bollinger Bands Calculation
# ==========================================================


def calculate_bollinger_bands(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
    std: float = DEFAULT_STD,
) -> pd.DataFrame:
    """
    Calculate Bollinger Bands.

    Returns
    -------
    DataFrame
        middle, upper, lower bands
    """

    _validate_dataframe(data)
    _validate_window(window)

    try:

        close = data[DEFAULT_COLUMN]

        ma = close.rolling(window=window).mean()

        std_dev = close.rolling(window=window).std()

        upper = ma + std * std_dev
        lower = ma - std * std_dev

        return pd.DataFrame(
            {
                "BB_Middle": ma,
                "BB_Upper": upper,
                "BB_Lower": lower,
            },
            index=data.index,
        )

    except Exception:

        logger.exception(
            "Failed calculating Bollinger Bands."
        )

        return pd.DataFrame(index=data.index)


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_bollinger(
    data: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
    std: float = DEFAULT_STD,
) -> pd.DataFrame:
    """
    Append Bollinger Bands columns.
    """

    df = data.copy()

    bands = calculate_bollinger_bands(
        df,
        window=window,
        std=std,
    )

    return df.join(bands)

# ==========================================================
# Bollinger State Detection
# ==========================================================


def is_upper_band_breakout(
    data: pd.DataFrame,
) -> bool:
    """
    Price breaks above upper band.
    """

    if "BB_Upper" not in data.columns:
        data = add_bollinger(data)

    latest = data.iloc[-1]

    return latest["Close"] > latest["BB_Upper"]


def is_lower_band_breakdown(
    data: pd.DataFrame,
) -> bool:
    """
    Price breaks below lower band.
    """

    if "BB_Lower" not in data.columns:
        data = add_bollinger(data)

    latest = data.iloc[-1]

    return latest["Close"] < latest["BB_Lower"]


# ==========================================================
# Bollinger Squeeze
# ==========================================================


def calculate_bandwidth(
    data: pd.DataFrame,
) -> float:
    """
    Bandwidth = (Upper - Lower) / Middle
    """

    if "BB_Middle" not in data.columns:
        data = add_bollinger(data)

    latest = data.iloc[-1]

    middle = latest["BB_Middle"]
    upper = latest["BB_Upper"]
    lower = latest["BB_Lower"]

    if middle == 0:
        return 0.0

    return float((upper - lower) / middle)


def is_squeeze(
    data: pd.DataFrame,
    threshold: float = 0.1,
) -> bool:
    """
    Low volatility squeeze condition.
    """

    bandwidth = calculate_bandwidth(data)

    return bandwidth < threshold


# ==========================================================
# Percent B (%B)
# ==========================================================


def calculate_percent_b(
    data: pd.DataFrame,
) -> float:
    """
    Position within bands.

    1 = upper band
    0 = lower band
    """

    if "BB_Middle" not in data.columns:
        data = add_bollinger(data)

    latest = data.iloc[-1]

    upper = latest["BB_Upper"]
    lower = latest["BB_Lower"]
    price = latest["Close"]

    if upper == lower:
        return 0.5

    return float((price - lower) / (upper - lower))


# ==========================================================
# Signal Engine
# ==========================================================


def get_bollinger_signal(
    data: pd.DataFrame,
) -> str:
    """
    Return volatility signal state.
    """

    if is_upper_band_breakout(data):
        return "Breakout Up"

    if is_lower_band_breakdown(data):
        return "Breakdown Down"

    if is_squeeze(data):
        return "Squeeze"

    percent_b = calculate_percent_b(data)

    if percent_b > 0.8:
        return "Upper Range"

    if percent_b < 0.2:
        return "Lower Range"

    return "Normal"
