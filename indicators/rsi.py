"""
MQD Dashboard
RSI Indicator
"""

import pandas as pd


def calculate_rsi(
    data: pd.DataFrame,
    window: int = 14
) -> pd.DataFrame:
    """
    RSI(Relative Strength Index) 계산
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    if "Close" not in data.columns:
        raise KeyError("Close column not found.")

    df = data.copy()

    close = df["Close"].astype(float)

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(
        window=window,
        min_periods=window
    ).mean()

    avg_loss = loss.rolling(
        window=window,
        min_periods=window
    ).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)

    df["RSI"] = (
        100
        - (100 / (1 + rs))
    ).astype(float)

    return df