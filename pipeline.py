"""
MQD v2 Pipeline Engine

Purpose
-------
Orchestrate full data flow:
- Data cleaning
- Indicator aggregation
- Feature preparation
- Signal consolidation

This module does NOT calculate MQD scores.

Python 3.12
"""

from __future__ import annotations

import logging

import pandas as pd

from indicators.moving_average import add_all_moving_averages
from indicators.rsi import add_rsi_features
from indicators.macd import add_macd_features
from indicators.bollinger import add_bollinger_features
from indicators.atr import add_atr_features
from indicators.mfi import add_mfi_features
from indicators.obv import add_obv_features
from indicators.vwap import add_vwap_features

logger = logging.getLogger(__name__)


# ==========================================================
# Data Cleaning
# ==========================================================


def clean_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Basic data cleaning step.

    - Sort index
    - Drop duplicates
    - Forward fill missing values
    """

    df = data.copy()

    try:

        df = df.sort_index()

        df = df[~df.index.duplicated(keep="last")]

        df = df.ffill()

        return df

    except Exception:

        logger.exception("Data cleaning failed.")

        return df

  # ==========================================================
# Indicator Pipeline
# ==========================================================


def apply_indicators(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply all MQD indicators to raw OHLCV data.
    """

    df = data.copy()

    try:

        # Trend Engine
        df = add_all_moving_averages(df)

        # Momentum Engine
        df = add_rsi_features(df)
        df = add_macd_features(df)

        # Volatility Engine
        df = add_bollinger_features(df)

        # Risk Engine
        df = add_atr_features(df)

        # Money Flow Engine
        df = add_mfi_features(df)

        # Volume Engine
        df = add_obv_features(df)

        # Fair Price Engine
        df = add_vwap_features(df)

        return df

    except Exception:

        logger.exception("Indicator application failed.")

        return df


# ==========================================================
# Feature Builder
# ==========================================================


def build_feature_dataframe(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build full feature-rich DataFrame for MQD scoring.
    """

    df = apply_indicators(data)

    return df


# ==========================================================
# Pipeline Entry
# ==========================================================


def run_pipeline(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Full MQD pipeline execution.

    Steps:
    1. Clean data
    2. Apply indicators
    3. Return feature-rich dataset
    """

    try:

        df = clean_data(data)

        df = build_feature_dataframe(df)

        return df

    except Exception:

        logger.exception("Pipeline execution failed.")

        return data

  # ==========================================================
# Signal Aggregation
# ==========================================================


def _safe_get(column: str, df: pd.DataFrame) -> pd.Series:
    """
    Safe column access helper.
    """

    if column in df.columns:
        return df[column]

    return pd.Series(
        False,
        index=df.index,
    )


# ==========================================================
# Market State Summary
# ==========================================================


def build_market_state(
    data: pd.DataFrame,
) -> dict[str, object]:
    """
    Aggregate all indicator signals into a single market state.
    """

    df = data.copy()

    try:

        latest = df.iloc[-1]

        state = {
            # Trend
            "trend_bullish": bool(
                latest.get("BullishAlignment", False)
            ),
            "trend_bearish": bool(
                latest.get("BearishAlignment", False)
            ),

            # Momentum
            "rsi": float(latest.get("RSI", 50)),
            "macd_bullish": bool(
                latest.get("MACD_Bullish", False)
            ),
            "macd_bearish": bool(
                latest.get("MACD_Bearish", False)
            ),

            # Volatility
            "bb_squeeze": bool(
                latest.get("BB_Squeeze", False)
            ),
            "bb_breakout_up": bool(
                latest.get("BB_Upper_Break", False)
            ),
            "bb_breakdown_down": bool(
                latest.get("BB_Lower_Break", False)
            ),

            # Risk
            "atr_pct": float(
                latest.get("ATR_Pct", 0)
            ),
            "high_volatility": bool(
                latest.get("High_Volatility", False)
            ),

            # Money Flow
            "mfi": float(latest.get("MFI", 50)),
            "mfi_bullish": bool(
                latest.get("MFI_Bullish", False)
            ),
            "mfi_bearish": bool(
                latest.get("MFI_Bearish", False)
            ),

            # Volume
            "obv_rising": bool(
                latest.get("OBV_Rising", False)
            ),
            "obv_breakout": bool(
                latest.get("OBV_Breakout", False)
            ),

            # Fair Price
            "above_vwap": bool(
                latest.get("Above_VWAP", False)
            ),
            "below_vwap": bool(
                latest.get("Below_VWAP", False)
            ),
        }

        return state

    except Exception:

        logger.exception("Market state build failed.")

        return {}

  # ==========================================================
# MQD Output Object
# ==========================================================


def build_mqd_output(
    data: pd.DataFrame,
) -> dict[str, object]:
    """
    Build final MQD-ready output structure.

    This is the main interface used by:
    - scoring/mqd_score.py
    - streamlit_app.py
    """

    try:

        df = run_pipeline(data)

        state = build_market_state(df)

        latest = df.iloc[-1]

        output = {
            # ==========================
            # Raw Data
            # ==========================
            "data": df,

            # ==========================
            # Market State
            # ==========================
            "state": state,

            # ==========================
            # Core Snapshot
            # ==========================
            "snapshot": {
                "close": float(latest.get("Close", 0)),
                "volume": float(latest.get("Volume", 0)),
                "rsi": float(latest.get("RSI", 50)),
                "macd": float(latest.get("MACD", 0)),
                "atr_pct": float(latest.get("ATR_Pct", 0)),
                "mfi": float(latest.get("MFI", 50)),
                "obv": float(latest.get("OBV", 0)),
                "vwap": float(latest.get("VWAP", 0)),
            },

            # ==========================
            # Feature Flags (Quick Access)
            # ==========================
            "flags": {
                "trend_bullish": state.get("trend_bullish", False),
                "trend_bearish": state.get("trend_bearish", False),
                "macd_bullish": state.get("macd_bullish", False),
                "macd_bearish": state.get("macd_bearish", False),
                "bb_squeeze": state.get("bb_squeeze", False),
                "high_volatility": state.get("high_volatility", False),
                "above_vwap": state.get("above_vwap", False),
                "below_vwap": state.get("below_vwap", False),
                "obv_breakout": state.get("obv_breakout", False),
                "mfi_bullish": state.get("mfi_bullish", False),
                "mfi_bearish": state.get("mfi_bearish", False),
            },
        }

        return output

    except Exception:

        logger.exception("MQD output build failed.")

        return {
            "data": data,
            "state": {},
            "snapshot": {},
            "flags": {},
        }


# ==========================================================
# Pipeline Runner (Public API)
# ==========================================================


def run_mqd_pipeline(
    data: pd.DataFrame,
) -> dict[str, object]:
    """
    Main public entry point for MQD system.

    Used by:
    - scoring engine
    - streamlit dashboard
    """

    return build_mqd_output(data)
