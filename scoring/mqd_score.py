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
    
df["MQD Score"] = 0

# ① 정배열
df.loc[
    (df["MA20"] > df["MA60"]) &
    (df["MA60"] > df["MA120"]),
    "MQD Score"
] += 30

# ② 현재가가 MA20 위
df.loc[
    df["Close"] > df["MA20"],
    "MQD Score"
] += 20

# ③ RSI 50~70
df.loc[
    (df["RSI"] >= 50) &
    (df["RSI"] <= 70),
    "MQD Score"
] += 20

# ④ RSI 30~50
df.loc[
    (df["RSI"] >= 30) &
    (df["RSI"] < 50),
    "MQD Score"
] += 10

# ⑤ MA20 상승
df.loc[
    df["MA20"] > df["MA20"].shift(1),
    "MQD Score"
] += 30

df["Confidence Score"] = df["MQD Score"]


    return df