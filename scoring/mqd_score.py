"""
MQD Score Engine

MQD v2

Purpose
-------
Convert market state into a unified score (0 ~ 100)

This module MUST NOT compute indicators.
It only consumes pipeline output.

Python 3.12
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


# ==========================================================
# Score Weights (MQD v2)
# ==========================================================

WEIGHTS = {
    "trend": 0.30,
    "momentum": 0.20,
    "money_flow": 0.20,
    "volume": 0.10,
    "volatility": 0.10,
    "risk": 0.10,
}

# ==========================================================
# Trend Score
# ==========================================================


def calculate_trend_score(state: dict) -> float:
    """
    Trend component score (0 ~ 100)
    Weight: 30%
    """

    score = 0.0

    try:

        # ==========================
        # Bullish Alignment
        # ==========================
        if state.get("trend_bullish"):
            score += 40

        # ==========================
        # Bearish Penalty
        # ==========================
        if state.get("trend_bearish"):
            score -= 40

        # ==========================
        # MACD Confirmation
        # ==========================
        if state.get("macd_bullish"):
            score += 20

        if state.get("macd_bearish"):
            score -= 20

        # ==========================
        # VWAP Bias
        # ==========================
        if state.get("above_vwap"):
            score += 20

        if state.get("below_vwap"):
            score -= 20

        # ==========================
        # Normalize (0 ~ 100)
        # ==========================
        score = 50 + score

        return max(0.0, min(100.0, score))

    except Exception:

        logger.exception("Trend score calculation failed.")

        return 50.0

# ==========================================================
# Momentum Score
# ==========================================================


def calculate_momentum_score(state: dict) -> float:
    """
    Momentum component score (0 ~ 100)
    Weight: 20%
    """

    score = 50.0

    try:

        # ==========================
        # RSI Contribution
        # ==========================
        rsi = state.get("rsi", 50)

        if rsi >= 70:
            score -= 15  # overbought risk

        elif rsi <= 30:
            score += 15  # oversold rebound potential

        elif 50 < rsi < 70:
            score += 10  # bullish momentum

        elif 30 < rsi < 50:
            score -= 10  # bearish pressure

        # ==========================
        # MACD Confirmation
        # ==========================
        if state.get("macd_bullish"):
            score += 20

        if state.get("macd_bearish"):
            score -= 20

        # ==========================
        # MFI (Money Flow Momentum)
        # ==========================
        mfi = state.get("mfi", 50)

        if mfi >= 80:
            score -= 10  # overheating

        elif mfi <= 20:
            score += 10  # accumulation zone

        elif mfi > 50:
            score += 10  # inflow strength

        else:
            score -= 10  # outflow pressure

        # ==========================
        # Normalize
        # ==========================
        return max(0.0, min(100.0, score))

    except Exception:

        logger.exception("Momentum score calculation failed.")

        return 50.0

# ==========================================================
# Money Flow + Volume Score
# ==========================================================


def calculate_money_flow_score(state: dict) -> float:
    """
    Money Flow + Volume score (0 ~ 100)
    Weight: 20%
    """

    score = 50.0

    try:

        # ==========================
        # MFI Contribution
        # ==========================
        mfi = state.get("mfi", 50)

        if mfi >= 80:
            score -= 15  # overbought distribution risk

        elif mfi <= 20:
            score += 20  # strong accumulation

        elif mfi > 50:
            score += 10  # inflow dominance

        else:
            score -= 10  # outflow pressure

        # ==========================
        # OBV Trend
        # ==========================
        if state.get("obv_rising"):
            score += 20

        if state.get("obv_falling"):
            score -= 20

        # ==========================
        # OBV Breakout (Strong signal)
        # ==========================
        if state.get("obv_breakout"):
            score += 10

        # ==========================
        # Combined interpretation boost
        # ==========================
        if state.get("mfi_bullish") and state.get("obv_rising"):
            score += 10

        if state.get("mfi_bearish") and state.get("obv_falling"):
            score -= 10

        # ==========================
        # Normalize
        # ==========================
        return max(0.0, min(100.0, score))

    except Exception:

        logger.exception("Money flow score calculation failed.")

        return 50.0

# ==========================================================
# Money Flow + Volume Score
# ==========================================================


def calculate_money_flow_score(state: dict) -> float:
    """
    Money Flow + Volume score (0 ~ 100)
    Weight: 20%
    """

    score = 50.0

    try:

        # ==========================
        # MFI Contribution
        # ==========================
        mfi = state.get("mfi", 50)

        if mfi >= 80:
            score -= 15  # overbought distribution risk

        elif mfi <= 20:
            score += 20  # strong accumulation

        elif mfi > 50:
            score += 10  # inflow dominance

        else:
            score -= 10  # outflow pressure

        # ==========================
        # OBV Trend
        # ==========================
        if state.get("obv_rising"):
            score += 20

        if state.get("obv_falling"):
            score -= 20

        # ==========================
        # OBV Breakout (Strong signal)
        # ==========================
        if state.get("obv_breakout"):
            score += 10

        # ==========================
        # Combined interpretation boost
        # ==========================
        if state.get("mfi_bullish") and state.get("obv_rising"):
            score += 10

        if state.get("mfi_bearish") and state.get("obv_falling"):
            score -= 10

        # ==========================
        # Normalize
        # ==========================
        return max(0.0, min(100.0, score))

    except Exception:

        logger.exception("Money flow score calculation failed.")

        return 50.0


# ==========================================================
# FINAL MQD SCORE
# ==========================================================


def calculate_mqd_score(state: dict) -> dict[str, float]:
    """
    Final MQD Score (0 ~ 100)

    Combines:
    - Trend (30%)
    - Momentum (20%)
    - Money Flow (20%)
    - Volume (10%)
    - Volatility/Risk (10%)
    """

    try:

        trend = calculate_trend_score(state)
        momentum = calculate_momentum_score(state)
        flow = calculate_money_flow_score(state)
        volatility = calculate_volatility_risk_score(state)

        # ==========================
        # Weighted Score
        # ==========================
        final_score = (
            trend * WEIGHTS["trend"]
            + momentum * WEIGHTS["momentum"]
            + flow * WEIGHTS["money_flow"]
            + volatility * (WEIGHTS["volatility"] + WEIGHTS["risk"])
        )

        final_score = max(0.0, min(100.0, final_score))

        # ==========================
        # Interpretation
        # ==========================
        if final_score >= 80:
            signal = "Strong Bullish"

        elif final_score >= 60:
            signal = "Bullish"

        elif final_score >= 40:
            signal = "Neutral"

        elif final_score >= 20:
            signal = "Bearish"

        else:
            signal = "Strong Bearish"

        return {
            "mqd_score": final_score,
            "signal": signal,
            "trend": trend,
            "momentum": momentum,
            "money_flow": flow,
            "volatility": volatility,
        }

    except Exception:

        logger.exception("Final MQD score calculation failed.")

        return {
            "mqd_score": 50.0,
            "signal": "Neutral",
            "trend": 50.0,
            "momentum": 50.0,
            "money_flow": 50.0,
            "volatility": 50.0,
        }
