"""
MQD Dashboard
Momentum Indicators
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_PERIOD = 14


def calculate_rate_of_change(
    data: pd.DataFrame,
    period: int = DEFAULT_PERIOD,
) -> pd.DataFrame:
    """
    Calculate Rate of Change (ROC).

    Parameters
    ----------
    data : pd.DataFrame
        Price DataFrame containing the Close column.

    period : int
        Lookback period.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with ROC column added.
    """

    logger.info("Calculating ROC")

    if data.empty:
        logger.error("Input DataFrame is empty.")
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        logger.error("Close column not found.")
        raise KeyError("Close column not found.")

    if period <= 0:
        logger.error("Invalid ROC period: %s", period)
        raise ValueError("Period must be greater than zero.")

    try:

        df = data.copy()

        close = df["Close"].astype(float)

        df["ROC"] = (
            close
            .pct_change(periods=period)
            * 100
        )

        logger.info("ROC calculated successfully")

        return df

    except Exception:
        logger.exception(
            "Failed to calculate ROC."
        )
        raise


def calculate_momentum(
    data: pd.DataFrame,
    period: int = DEFAULT_PERIOD,
) -> pd.DataFrame:
    """
    Calculate Momentum.

    Parameters
    ----------
    data : pd.DataFrame
        Price DataFrame containing the Close column.

    period : int
        Lookback period.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with Momentum column added.
    """

    logger.info("Calculating Momentum")

    if data.empty:
        logger.error("Input DataFrame is empty.")
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        logger.error("Close column not found.")
        raise KeyError("Close column not found.")

    if period <= 0:
        logger.error("Invalid Momentum period: %s", period)
        raise ValueError("Period must be greater than zero.")

    try:

        df = data.copy()

        close = df["Close"].astype(float)

        df["Momentum"] = close.diff(periods=period)

        logger.info("Momentum calculated successfully")

        return df

    except Exception:
        logger.exception(
            "Failed to calculate Momentum."
        )
        raise
