"""
MQD Dashboard
Moving Average Indicator
"""

import pandas as pd


def calculate_moving_average(
    data: pd.DataFrame,
    windows: list[int] = [20, 60, 120]
) -> pd.DataFrame:
    """
    이동평균(Moving Average)을 계산한다.

    Parameters
    ----------
    data : pandas.DataFrame
        Yahoo Finance 가격 데이터

    windows : list[int]
        계산할 이동평균 기간

    Returns
    -------
    pandas.DataFrame
        이동평균 컬럼이 추가된 데이터
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    df = data.copy()

    for window in windows:
        column = f"MA{window}"
        df[column] = df["Close"].rolling(window=window).mean()

    return df