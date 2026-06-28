"""
MQD Dashboard
Moving Average Indicator
"""

import pandas as pd


DEFAULT_WINDOWS = (20, 60, 120)


def calculate_moving_average(
    data: pd.DataFrame,
    windows: tuple[int, ...] = DEFAULT_WINDOWS,
) -> pd.DataFrame:
    """
    이동평균(MA)을 계산한다.
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        raise KeyError("Close column not found.")

    df = data.copy()

    close = df["Close"].astype(float)

    for window in windows:

        if window <= 0:
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

    return df