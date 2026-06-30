"""
MQD Asset Universe

Supported Assets
----------------
- Korea
- US
- Global Index
- ETF
- Currency
- Commodity
- Crypto

Author
------
MQD Project
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Asset:
    """Represents a market asset."""

    name: str
    ticker: str
    category: str
    market: str


ALL_ASSETS: Dict[str, Asset] = {
    # ==========================
    # Korea
    # ==========================
    "Samsung Electronics": Asset(
        "Samsung Electronics",
        "005930.KS",
        "Stock",
        "Korea",
    ),
    "SK Hynix": Asset(
        "SK Hynix",
        "000660.KS",
        "Stock",
        "Korea",
    ),
    "LG Energy Solution": Asset(
        "LG Energy Solution",
        "373220.KS",
        "Stock",
        "Korea",
    ),
    "Hyundai Motor": Asset(
        "Hyundai Motor",
        "005380.KS",
        "Stock",
        "Korea",
    ),
    "NAVER": Asset(
        "NAVER",
        "035420.KS",
        "Stock",
        "Korea",
    ),
    "Kakao": Asset(
        "Kakao",
        "035720.KS",
        "Stock",
        "Korea",
    ),

    # ==========================
    # United States
    # ==========================
    "Apple": Asset(
        "Apple",
        "AAPL",
        "Stock",
        "USA",
    ),
    "Microsoft": Asset(
        "Microsoft",
        "MSFT",
        "Stock",
        "USA",
    ),
    "NVIDIA": Asset(
        "NVIDIA",
        "NVDA",
        "Stock",
        "USA",
    ),
    "Amazon": Asset(
        "Amazon",
        "AMZN",
        "Stock",
        "USA",
    ),
    "Alphabet": Asset(
        "Alphabet",
        "GOOGL",
        "Stock",
        "USA",
    ),
    "Tesla": Asset(
        "Tesla",
        "TSLA",
        "Stock",
        "USA",
    ),
    "Meta": Asset(
        "Meta",
        "META",
        "Stock",
        "USA",
    ),

    # ==========================
    # Global Index
    # ==========================
    "KOSPI": Asset(
        "KOSPI",
        "^KS11",
        "Index",
        "Korea",
    ),
    "KOSDAQ": Asset(
        "KOSDAQ",
        "^KQ11",
        "Index",
        "Korea",
    ),
    "S&P 500": Asset(
        "S&P 500",
        "^GSPC",
        "Index",
        "USA",
    ),
    "NASDAQ": Asset(
        "NASDAQ",
        "^IXIC",
        "Index",
        "USA",
    ),
    "Dow Jones": Asset(
        "Dow Jones",
        "^DJI",
        "Index",
        "USA",
    ),
    "Russell 2000": Asset(
        "Russell 2000",
        "^RUT",
        "Index",
        "USA",
    ),
    "Nikkei 225": Asset(
        "Nikkei 225",
        "^N225",
        "Index",
        "Japan",
    ),
    "Hang Seng": Asset(
        "Hang Seng",
        "^HSI",
        "Index",
        "Hong Kong",
    ),
    "DAX": Asset(
        "DAX",
        "^GDAXI",
        "Index",
        "Germany",
    ),
    "FTSE 100": Asset(
        "FTSE 100",
        "^FTSE",
        "Index",
        "United Kingdom",
    ),

    # ==========================
    # ETF
    # ==========================
    "SPY": Asset(
        "SPY",
        "SPY",
        "ETF",
        "USA",
    ),
    "QQQ": Asset(
        "QQQ",
        "QQQ",
        "ETF",
        "USA",
    ),
    "DIA": Asset(
        "DIA",
        "DIA",
        "ETF",
        "USA",
    ),
    "IWM": Asset(
        "IWM",
        "IWM",
        "ETF",
        "USA",
    ),
    "SOXX": Asset(
        "SOXX",
        "SOXX",
        "ETF",
        "USA",
    ),

    # ==========================
    # Currency
    # ==========================
    "USD/KRW": Asset(
        "USD/KRW",
        "KRW=X",
        "FX",
        "Global",
    ),
    "EUR/USD": Asset(
        "EUR/USD",
        "EURUSD=X",
        "FX",
        "Global",
    ),
    "JPY/USD": Asset(
        "JPY/USD",
        "JPY=X",
        "FX",
        "Global",
    ),

    # ==========================
    # Commodity
    # ==========================
    "Gold": Asset(
        "Gold",
        "GC=F",
        "Commodity",
        "Global",
    ),
    "Silver": Asset(
        "Silver",
        "SI=F",
        "Commodity",
        "Global",
    ),
    "Crude Oil": Asset(
        "Crude Oil",
        "CL=F",
        "Commodity",
        "Global",
    ),
    "Natural Gas": Asset(
        "Natural Gas",
        "NG=F",
        "Commodity",
        "Global",
    ),

    # ==========================
    # Crypto
    # ==========================
    "Bitcoin": Asset(
        "Bitcoin",
        "BTC-USD",
        "Crypto",
        "Global",
    ),
    "Ethereum": Asset(
        "Ethereum",
        "ETH-USD",
        "Crypto",
        "Global",
    ),
    "Solana": Asset(
        "Solana",
        "SOL-USD",
        "Crypto",
        "Global",
    ),
    "XRP": Asset(
        "XRP",
        "XRP-USD",
        "Crypto",
        "Global",
    ),
}


def get_asset(name: str) -> Asset:
    """
    Return Asset by display name.

    Raises
    ------
    KeyError
        If asset is not registered.
    """
    return ALL_ASSETS[name]


def get_ticker(name: str) -> str:
    """
    Return Yahoo Finance ticker.
    """
    return get_asset(name).ticker


def get_asset_names() -> list[str]:
    """
    Returns all display names.
    """
    return list(ALL_ASSETS.keys())


def get_assets_by_category(category: str) -> dict[str, Asset]:
    """
    Filter assets by category.
    """
    return {
        k: v
        for k, v in ALL_ASSETS.items()
        if v.category.lower() == category.lower()
    }
