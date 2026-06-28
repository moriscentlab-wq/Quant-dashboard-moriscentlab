"""
MQD Dashboard
MQD Score Engine
"""

import pandas as pd


def calculate_mqd_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    MQD Score 계산을 위한 기본 엔진.

    실제 점수 규칙은 프로젝트 정책에 따라
    이후 단계에서 추가한다.
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    df = data.copy()

    score = 0

    # --------------------------
    # RSI
    # --------------------------
    if "RSI" in df.columns:
        latest_rsi = df["RSI"].iloc[-1]

        if latest_rsi >= 50:
            score += 1

    # --------------------------
    # Moving Average
    # --------------------------
    ma_columns = {"MA20", "MA60", "MA120"}

    if ma_columns.issubset(df.columns):

        latest = df.iloc[-1]

        if (
            latest["MA20"] > latest["MA60"]
            and latest["MA60"] > latest["MA120"]
        ):
            score += 1

    df["MQD Score"] = score

    return df