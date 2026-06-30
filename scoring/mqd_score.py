"""
MQD Dashboard
MQD Score Engine
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Close",
    "MA20",
    "MA60",
    "MA120",
    "RSI",
    "Momentum",
    "ROC",
]


def calculate_mqd_score(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate MQD Score and Confidence Score.

    Returns
    -------
    pd.DataFrame
        Original DataFrame with
        MQD Score
        Confidence Score
    """

    logger.info("Calculating MQD Score")

    if data.empty:
        raise ValueError("DataFrame is empty.")

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise KeyError(
            f"Missing columns: {missing}"
        )

    try:

        df = data.copy()

        scores = []
        confidence_scores = []

        for i in range(len(df)):

            row = df.iloc[i]

            score = 0

            confidence = 0

            # -----------------------------
            # MA Trend
            # -----------------------------

            if (
                pd.notna(row["MA20"])
                and pd.notna(row["MA60"])
                and pd.notna(row["MA120"])
            ):

                if (
                    row["MA20"]
                    > row["MA60"]
                    > row["MA120"]
                ):
                    score += 25
                    confidence += 20

            # -----------------------------
            # Close > MA20
            # -----------------------------

            if (
                pd.notna(row["MA20"])
                and row["Close"] > row["MA20"]
            ):
                score += 15
                confidence += 15

            # -----------------------------
            # RSI
            # -----------------------------

            if pd.notna(row["RSI"]):

                if 50 <= row["RSI"] <= 70:
                    score += 20
                    confidence += 20

                elif 40 <= row["RSI"] < 50:
                    score += 10
                    confidence += 10

            # -----------------------------
            # MA20 Rising
            # -----------------------------

            if i > 0:

                previous_ma20 = df.iloc[i - 1]["MA20"]

                if (
                    pd.notna(previous_ma20)
                    and pd.notna(row["MA20"])
                    and row["MA20"] > previous_ma20
                ):
                    score += 20
                    confidence += 15

            # -----------------------------
            # Momentum
            # -----------------------------

            if (
                pd.notna(row["Momentum"])
                and row["Momentum"] > 0
            ):
                score += 10
                confidence += 10

            # -----------------------------
            # ROC
            # -----------------------------

            if (
                pd.notna(row["ROC"])
                and row["ROC"] > 0
            ):
                score += 10
                confidence += 10

            scores.append(min(score, 100))

            confidence_scores.append(
                min(confidence, 100)
            )

        df["MQD Score"] = scores

        df["Confidence Score"] = confidence_scores

        logger.info(
            "MQD Score calculated successfully"
        )

        return df

    except Exception:

        logger.exception(
            "MQD Score calculation failed."
        )

        raise
