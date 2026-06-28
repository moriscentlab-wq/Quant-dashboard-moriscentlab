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
    RSI(Relative Strength Index)를 계산한다.

    Parameters
    ----------
    data : pandas.DataFrame
        Yahoo Finance 가격 데이터

    window : int
        RSI 기간 (기본 14)

    Returns
    -------
    pandas.DataFrame
        RSI 컬럼이 추가된 데이터
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    df = data.copy()

    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)

    df["RSI"] = 100 - (100 / (1 + rs))

    return df