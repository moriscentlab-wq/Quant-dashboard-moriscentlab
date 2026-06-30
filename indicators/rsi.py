"""
MQD Dashboard
Relative Strength Index (RSI) Indicator
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_PERIOD = 14


def calculate_rsi(
    data: pd.DataFrame,
    period: int = DEFAULT_PERIOD,
) -> pd.DataFrame:
    """
    Calculate Relative Strength Index (RSI).

    Parameters
    ----------
    data : pd.DataFrame
        Price DataFrame containing the Close column.

    period : int
        RSI lookback period.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with RSI column added.

    Raises
    ------
    ValueError
        If DataFrame is empty or period is invalid.

    KeyError
        If Close column is missing.
    """

    logger.info("Calculating RSI")

    if data.empty:
        logger.error("Input DataFrame is empty.")
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        logger.error("Close column not found.")
        raise KeyError("Close column not found.")

    if period <= 0:
        logger.error("Invalid RSI period: %s", period)
        raise ValueError("Period must be greater than zero.")

    try:

        df = data.copy()

        close = df["Close"].astype(float)

        delta = close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        average_gain = gain.rolling(
            window=period,
            min_periods=period,
        ).mean()

        average_loss = loss.rolling(
            window=period,
            min_periods=period,
        ).mean()

        rs = average_gain / average_loss

        rsi = 100 - (100 / (1 + rs))

        # Handle division by zero safely
        rsi = rsi.where(
            ~(average_loss.eq(0) & average_gain.gt(0)),
            100,
        )

        rsi = rsi.where(
            ~(average_gain.eq(0) & average_loss.gt(0)),
            0,
        )

        rsi = rsi.where(
            ~(average_gain.eq(0) & average_loss.eq(0)),
            50,
        )

        df["RSI"] = rsi.clip(0, 100)

        logger.info("RSI calculated successfully")

        return df

    except Exception:
        logger.exception("Failed to calculate RSI.")
        raise
