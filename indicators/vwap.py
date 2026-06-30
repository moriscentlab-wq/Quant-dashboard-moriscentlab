"""
Volume Weighted Average Price (VWAP)

MQD v2 Indicator

Purpose
-------
- Institutional fair price level
- Intraday / trend reference price
- Market bias detection

This module DOES NOT calculate MQD scores.

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
    Validate OHLCV DataFrame.
    """

    required = ["High", "Low", "Close", "Volume"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


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
# VWAP Calculation
# ==========================================================


def calculate_vwap(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Calculate VWAP.

    VWAP = cumulative(TP * Volume) / cumulative(Volume)
    """

    _validate_dataframe(data)

    try:

        tp = calculate_typical_price(data)

        cum_vol = data["Volume"].cumsum()

        cum_pv = (tp * data["Volume"]).cumsum()

        vwap = cum_pv / cum_vol.replace(0, np.nan)

        return vwap.fillna(method="ffill")

    except Exception:

        logger.exception(
            "Failed calculating VWAP."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_vwap(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append VWAP column.
    """

    df = data.copy()

    df["VWAP"] = calculate_vwap(df)

    return df

"""
Volume Weighted Average Price (VWAP)

MQD v2 Indicator

Purpose
-------
- Institutional fair price level
- Intraday / trend reference price
- Market bias detection

This module DOES NOT calculate MQD scores.

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
    Validate OHLCV DataFrame.
    """

    required = ["High", "Low", "Close", "Volume"]

    if data.empty:
        raise ValueError("DataFrame is empty.")

    for col in required:
        if col not in data.columns:
            raise KeyError(f"{col} column not found.")


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
# VWAP Calculation
# ==========================================================


def calculate_vwap(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Calculate VWAP.

    VWAP = cumulative(TP * Volume) / cumulative(Volume)
    """

    _validate_dataframe(data)

    try:

        tp = calculate_typical_price(data)

        cum_vol = data["Volume"].cumsum()

        cum_pv = (tp * data["Volume"]).cumsum()

        vwap = cum_pv / cum_vol.replace(0, np.nan)

        return vwap.fillna(method="ffill")

    except Exception:

        logger.exception(
            "Failed calculating VWAP."
        )

        return pd.Series(
            dtype=float,
            index=data.index,
        )


# ==========================================================
# DataFrame Helper
# ==========================================================


def add_vwap(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Append VWAP column.
    """

    df = data.copy()

    df["VWAP"] = calculate_vwap(df)

    return df
