"""
MQD Dashboard
Moving Average Indicator
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_WINDOWS: tuple[int, ...] = (20, 60, 120)


def calculate_moving_average(
    data: pd.DataFrame,
    windows: tuple[int, ...] = DEFAULT_WINDOWS,
) -> pd.DataFrame:
    """
    Calculate moving averages for the specified windows.

    Parameters
    ----------
    data : pd.DataFrame
        Price DataFrame containing the Close column.
    windows : tuple[int, ...], optional
        Moving average periods.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with MA columns added.

    Raises
    ------
    ValueError
        If the DataFrame is empty or an invalid window is supplied.
    KeyError
        If the Close column is missing.
    """

    logger.info("Calculating moving averages")

    if data.empty:
        logger.error("Input DataFrame is empty.")
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        logger.error("Close column not found.")
        raise KeyError("Close column not found.")

    try:
        df = data.copy()

        close = df["Close"].astype(float)

        for window in windows:

            if window <= 0:
                logger.error(
                    "Invalid moving average window: %s",
                    window,
                )
                raise ValueError(
                    f"Invalid moving average window: {window}"
                )

            column = f"MA{window}"

            df[column] = (
                close
                .rolling(
                    window=window,
                    min_periods=window,
                )
                .mean()
            )

        logger.info("Moving averages calculated successfully")

        return df

    except Exception:
        logger.exception("Moving average calculation failed.")
        raise
