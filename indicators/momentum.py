"""Momentum indicator calculator."""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class MomentumCalculator:
    """Calculates momentum indicators.
    
    Evaluates rate of change and velocity of price movements.
    """
    
    def __init__(self):
        """Initialize calculator."""
        pass
    
    def calculate_rate_of_change(
        self,
        data: pd.DataFrame,
        period: int = 14
    ) -> pd.DataFrame:
        """Calculate Rate of Change (ROC).
        
        ROC = ((Close - Close[n periods ago]) / Close[n periods ago]) * 100
        
        Args:
            data: DataFrame with Close column.
            period: Lookback period.
            
        Returns:
            DataFrame with ROC column.
        """
        if data.empty or "Close" not in data.columns:
            logger.error("Invalid data for ROC calculation")
            return data
        
        try:
            df = data.copy()
            df["ROC"] = df["Close"].pct_change(periods=period) * 100
            logger.debug(f"Calculated ROC (period={period}) for {len(df)} records")
            return df
        
        except Exception as e:
            logger.error(f"ROC calculation failed: {e}")
            return data
    
    def calculate_momentum(
        self,
        data: pd.DataFrame,
        period: int = 14
    ) -> pd.DataFrame:
        """Calculate Momentum.
        
        Momentum = Close - Close[n periods ago]
        
        Args:
            data: DataFrame with Close column.
            period: Lookback period.
            
        Returns:
            DataFrame with Momentum column.
        """
        if data.empty or "Close" not in data.columns:
            logger.error("Invalid data for Momentum calculation")
            return data
        
        try:
            df = data.copy()
            df["Momentum"] = df["Close"].diff(periods=period)
            logger.debug(f"Calculated Momentum (period={period}) for {len(df)} records")
            return df
        
        except Exception as e:
            logger.error(f"Momentum calculation failed: {e}")
            return data
    
    def is_positive_momentum(self, momentum: float) -> bool:
        """Check if momentum is positive.
        
        Args:
            momentum: Momentum value.
            
        Returns:
            True if positive.
        """
        return momentum > 0
    
    def get_momentum_signal(self, data: pd.DataFrame, rsi: Optional[float] = None) -> Optional[str]:
        """Get momentum trading signal.
        
        Args:
            data: DataFrame with momentum indicators.
            rsi: Optional RSI value.
            
        Returns:
            'strong_buy', 'buy', 'neutral', 'sell', 'strong_sell', or None.
        """
        try:
            signals = []
            
            # Check ROC
            if "ROC" in data.columns and not data.empty:
                latest_roc = data["ROC"].iloc[-1]
                if not pd.isna(latest_roc):
                    if latest_roc > 5:
                        signals.append("buy")
                    elif latest_roc < -5:
                        signals.append("sell")
                    else:
                        signals.append("neutral")
            
            # Check RSI momentum >= 50 (from requirements)
            if rsi is not None:
                if rsi >= 50:
                    signals.append("buy")
                else:
                    signals.append("sell")
            
            if not signals:
                return None
            
            # Aggregate signals
            buy_count = signals.count("buy")
            sell_count = signals.count("sell")
            
            if buy_count > sell_count:
                return "buy" if buy_count == 1 else "strong_buy"
            elif sell_count > buy_count:
                return "sell" if sell_count == 1 else "strong_sell"
            else:
                return "neutral"
        
        except Exception as e:
            logger.error(f"Momentum signal calculation failed: {e}")
            return None
