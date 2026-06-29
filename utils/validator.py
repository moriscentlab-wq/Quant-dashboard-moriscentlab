"""Data validation utilities."""

import logging
import re
from typing import Optional, List
import pandas as pd

from config.constants import DATA_VALIDATION

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data quality and integrity."""
    
    @staticmethod
    def validate_ohlcv_dataframe(data: pd.DataFrame) -> bool:
        """Validate OHLCV DataFrame structure.
        
        Args:
            data: DataFrame to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        
        if not isinstance(data, pd.DataFrame):
            logger.error("Input is not a DataFrame")
            return False
        
        if data.empty:
            logger.error("DataFrame is empty")
            return False
        
        if not all(col in data.columns for col in required_cols):
            logger.error(f"Missing required columns: {required_cols}")
            return False
        
        return True
    
    @staticmethod
    def check_missing_data(data: pd.DataFrame) -> bool:
        """Check if missing data exceeds threshold.
        
        Args:
            data: DataFrame to check.
            
        Returns:
            True if data quality is acceptable.
        """
        if data.empty:
            return False
        
        total_cells = len(data) * len(data.columns)
        missing_cells = data.isna().sum().sum()
        missing_pct = missing_cells / total_cells if total_cells > 0 else 0
        
        threshold = DATA_VALIDATION["max_missing_data_pct"]
        
        if missing_pct > threshold:
            logger.warning(
                f"Missing data: {missing_pct*100:.1f}% (threshold: {threshold*100:.1f}%)"
            )
            return False
        
        return True
    
    @staticmethod
    def check_price_validity(data: pd.DataFrame) -> bool:
        """Check if prices are within valid range.
        
        Args:
            data: DataFrame with price data.
            
        Returns:
            True if prices are valid.
        """
        price_cols = ["Open", "High", "Low", "Close"]
        min_price = DATA_VALIDATION["min_price"]
        
        for col in price_cols:
            if col in data.columns:
                if (data[col] < min_price).any():
                    logger.warning(f"Prices below minimum threshold in {col}")
                    return False
        
        return True
    
    @staticmethod
    def check_price_gaps(data: pd.DataFrame) -> bool:
        """Check for abnormal price gaps.
        
        Args:
            data: DataFrame with price data.
            
        Returns:
            True if gaps are within acceptable range.
        """
        if len(data) < 2 or "Close" not in data.columns:
            return True
        
        max_gap = DATA_VALIDATION["max_price_gap_pct"]
        
        price_changes = data["Close"].pct_change().abs()
        if (price_changes > max_gap).any():
            logger.warning(f"Price gap exceeds threshold: {max_gap*100:.1f}%")
            return False
        
        return True
    
    @staticmethod
    def validate_all(data: pd.DataFrame) -> bool:
        """Run all validation checks.
        
        Args:
            data: DataFrame to validate.
            
        Returns:
            True if all checks pass.
        """
        checks = [
            ("OHLCV structure", DataValidator.validate_ohlcv_dataframe(data)),
            ("Missing data", DataValidator.check_missing_data(data)),
            ("Price validity", DataValidator.check_price_validity(data)),
            ("Price gaps", DataValidator.check_price_gaps(data)),
        ]
        
        all_passed = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            logger.info(f"{status} {check_name}")
            if not result:
                all_passed = False
        
        return all_passed


class TickerValidator:
    """Validates ticker symbols and formats."""
    
    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        """Validate ticker format.
        
        Args:
            ticker: Ticker symbol.
            
        Returns:
            True if valid format.
        """
        if not isinstance(ticker, str) or not ticker:
            return False
        
        # Allow alphanumeric, hyphens, dots, equals
        pattern = r'^[A-Z0-9\-\.=]+$'
        return bool(re.match(pattern, ticker.upper()))
    
    @staticmethod
    def normalize_ticker(ticker: str) -> str:
        """Normalize ticker to uppercase.
        
        Args:
            ticker: Ticker symbol.
            
        Returns:
            Normalized ticker.
        """
        return ticker.upper().strip()
    
    @staticmethod
    def validate_tickers(tickers: List[str]) -> tuple[List[str], List[str]]:
        """Validate list of tickers.
        
        Args:
            tickers: List of ticker symbols.
            
        Returns:
            Tuple of (valid_tickers, invalid_tickers).
        """
        valid = []
        invalid = []
        
        for ticker in tickers:
            if TickerValidator.is_valid_ticker(ticker):
                valid.append(TickerValidator.normalize_ticker(ticker))
            else:
                invalid.append(ticker)
        
        return valid, invalid
    
    @staticmethod
    def get_crypto_ticker(symbol: str) -> str:
        """Convert crypto symbol to Yahoo Finance ticker.
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH').
            
        Returns:
            Yahoo Finance ticker.
        """
        symbol = symbol.upper()
        return f"{symbol}-USD"
    
    @staticmethod
    def get_korean_ticker(code: str) -> str:
        """Convert Korean stock code to ticker.
        
        Args:
            code: 6-digit stock code.
            
        Returns:
            Formatted ticker.
        """
        return code.zfill(6)
