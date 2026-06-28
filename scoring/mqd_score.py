"""
MQD Dashboard
MQD Score Engine
"""

import pandas as pd


def calculate_mqd_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    MQD Score 계산 엔진

    실제 점수 계산 로직은
    MQD 공식 확정 후 추가한다.
    """

    if data.empty:
        raise ValueError("DataFrame is empty.")

    df = data.copy()

    if "RSI" not in df.columns:
        raise KeyError("RSI column not found.")

    for column in ("MA20", "MA60", "MA120"):
        if column not in df.columns:
            raise KeyError(f"{column} column not found.")

    # -------------------------
    # MQD Score (임시 골격)
    # -------------------------
    df["MQD Score"] = 0

    # -------------------------
    # Confidence Score (임시 골격)
    # -------------------------
    df["Confidence Score"] = 0

    return df