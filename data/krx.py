"""Korea Exchange (KRX) data collector."""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

from config.settings import settings
from config.constants import CACHE_CONFIG
from data.cache import DataCache

logger = logging.getLogger(__name__)


class KRXDataCollector:
    """Collects data from Korea Exchange (KRX).
    
    Provides Korean stock market data including KOSPI, KOSDAQ indices.
    Requires pykrx library for data access.
    """
    
    def __init__(self, cache: Optional[DataCache] = None):
        """Initialize KRX collector.
        
        Args:
            cache: DataCache instance.
        """
        self.cache = cache or DataCache()
        
        try:
            from pykrx import stock
            self.stock = stock
            self.available = True
        except ImportError:
            logger.warning("pykrx library not installed. KRX functionality limited.")
            self.stock = None
            self.available = False
    
    def get_historical_data(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True
    ) -> Optional[pd.DataFrame]:
        """Fetch historical price data for Korean stocks.
        
        Args:
            ticker: Korean stock ticker (e.g., '005930' for Samsung).
            start_date: Start date (YYYYMMDD format).
            end_date: End date (YYYYMMDD format).
            use_cache: Whether to use cached data.
            
        Returns:
            DataFrame with OHLCV data or None if failed.
        """
        if not self.available:
            logger.error("KRX data not available: pykrx not installed")
            return None
        
        cache_key = f"krx_hist_{ticker}_{start_date}_{end_date}"
        
        if use_cache and self.cache.exists(cache_key):
            logger.debug(f"Using cached KRX data for {ticker}")
            return self.cache.get(cache_key)
        
        try:
            # Default to last 1 year if dates not provided
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            
            data = self.stock.get_market_ohlcv(start_date, end_date, ticker)
            
            if data.empty:
                logger.warning(f"No KRX data for {ticker}")
                return None
            
            # Normalize column names
            data.columns = [col.lower().replace(" ", "_") for col in data.columns]
            
            # Cache
            self.cache.set(cache_key, data, ttl=CACHE_CONFIG["daily_data_ttl"])
            logger.info(f"Retrieved {len(data)} KRX records for {ticker}")
            return data
        
        except Exception as e:
            logger.error(f"Failed to retrieve KRX data for {ticker}: {e}")
            return None
    
    def get_kospi_stocks(self, use_cache: bool = True) -> Optional[pd.DataFrame]:
        """Get list of all KOSPI stocks.
        
        Args:
            use_cache: Whether to use cached data.
            
        Returns:
            DataFrame with stock list or None if failed.
        """
        if not self.available:
            logger.error("KRX data not available")
            return None
        
        cache_key = "krx_kospi_stocks"
        
        if use_cache and self.cache.exists(cache_key):
            return self.cache.get(cache_key)
        
        try:
            data = self.stock.get_market_ticker_list(market="KOSPI")
            df = pd.DataFrame({"ticker": data})
            
            self.cache.set(cache_key, df, ttl=CACHE_CONFIG["market_info_ttl"])
            return df
        
        except Exception as e:
            logger.error(f"Failed to get KOSPI stocks: {e}")
            return None
    
    def get_kosdaq_stocks(self, use_cache: bool = True) -> Optional[pd.DataFrame]:
        """Get list of all KOSDAQ stocks.
        
        Args:
            use_cache: Whether to use cached data.
            
        Returns:
            DataFrame with stock list or None if failed.
        """
        if not self.available:
            logger.error("KRX data not available")
            return None
        
        cache_key = "krx_kosdaq_stocks"
        
        if use_cache and self.cache.exists(cache_key):
            return self.cache.get(cache_key)
        
        try:
            data = self.stock.get_market_ticker_list(market="KOSDAQ")
            df = pd.DataFrame({"ticker": data})
            
            self.cache.set(cache_key, df, ttl=CACHE_CONFIG["market_info_ttl"])
            return df
        
        except Exception as e:
            logger.error(f"Failed to get KOSDAQ stocks: {e}")
            return None
    
    def get_daily_trading_value(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True
    ) -> Optional[pd.DataFrame]:
        """Get daily trading value for all stocks.
        
        Args:
            start_date: Start date (YYYYMMDD).
            end_date: End date (YYYYMMDD).
            use_cache: Whether to use cached data.
            
        Returns:
            DataFrame with trading values or None if failed.
        """
        if not self.available:
            logger.error("KRX data not available")
            return None
        
        cache_key = f"krx_trading_value_{start_date}_{end_date}"
        
        if use_cache and self.cache.exists(cache_key):
            return self.cache.get(cache_key)
        
        try:
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
            
            data = self.stock.get_market_trading_value_by_date(
                start_date,
                end_date,
                market="ALL"
            )
            
            if data.empty:
                return None
            
            self.cache.set(cache_key, data, ttl=CACHE_CONFIG["daily_data_ttl"])
            return data
        
        except Exception as e:
            logger.error(f"Failed to get KRX trading value: {e}")
            return None
    
    def validate_ticker(self, ticker: str) -> bool:
        """Validate Korean stock ticker.
        
        Args:
            ticker: Stock ticker (6-digit code).
            
        Returns:
            True if valid, False otherwise.
        """
        if not self.available:
            return False
        
        try:
            # Try to fetch 1 day of data
            today = datetime.now().strftime("%Y%m%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            
            data = self.stock.get_market_ohlcv(yesterday, today, ticker)
            return not data.empty
        except Exception:
            return False
