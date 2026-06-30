"""
MQD v2 Asset Universe

Supported Markets
-----------------
- Korea
- United States
- Global

Supported Asset Classes
-----------------------
- Stock
- ETF
- Index
- FX
- Commodity
- Bond
- Crypto

Python
------
Python 3.12

Author
------
MQD Project
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


# ==========================================================
# Asset Model
# ==========================================================

@dataclass(frozen=True, slots=True)
class Asset:
    """
    Market Asset
    """

    name: str
    ticker: str
    category: str
    market: str


# ==========================================================
# Categories
# ==========================================================

CATEGORY_STOCK = "Stock"
CATEGORY_ETF = "ETF"
CATEGORY_INDEX = "Index"
CATEGORY_FX = "FX"
CATEGORY_COMMODITY = "Commodity"
CATEGORY_BOND = "Bond"
CATEGORY_CRYPTO = "Crypto"


# ==========================================================
# Markets
# ==========================================================

MARKET_KOREA = "Korea"
MARKET_USA = "USA"
MARKET_GLOBAL = "Global"
MARKET_JAPAN = "Japan"
MARKET_CHINA = "China"
MARKET_HONGKONG = "Hong Kong"
MARKET_TAIWAN = "Taiwan"
MARKET_GERMANY = "Germany"
MARKET_FRANCE = "France"
MARKET_UK = "United Kingdom"
MARKET_INDIA = "India"


# ==========================================================
# Korea Stocks
# ==========================================================

KOREA_STOCKS: Dict[str, Asset] = {}


# ==========================================================
# USA Stocks
# ==========================================================

US_STOCKS: Dict[str, Asset] = {}


# ==========================================================
# Global Indices
# ==========================================================

GLOBAL_INDICES: Dict[str, Asset] = {}


# ==========================================================
# ETFs
# ==========================================================

ETFS: Dict[str, Asset] = {}


# ==========================================================
# Foreign Exchange
# ==========================================================

FX: Dict[str, Asset] = {}


# ==========================================================
# Commodities
# ==========================================================

COMMODITIES: Dict[str, Asset] = {}


# ==========================================================
# Bonds
# ==========================================================

BONDS: Dict[str, Asset] = {}


# ==========================================================
# Crypto
# ==========================================================

CRYPTO: Dict[str, Asset] = {}


# ==========================================================
# Internal Helper
# ==========================================================

def _asset(
    name: str,
    ticker: str,
    category: str,
    market: str,
) -> Asset:
    """
    Create Asset instance.
    """

    return Asset(
        name=name,
        ticker=ticker,
        category=category,
        market=market,
    )

# ==========================================================
# Korea Stocks
# ==========================================================

KOREA_STOCKS.update(
    {
        "Samsung Electronics": _asset(
            "Samsung Electronics",
            "005930.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "SK Hynix": _asset(
            "SK Hynix",
            "000660.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "LG Energy Solution": _asset(
            "LG Energy Solution",
            "373220.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Samsung Biologics": _asset(
            "Samsung Biologics",
            "207940.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Hyundai Motor": _asset(
            "Hyundai Motor",
            "005380.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Kia": _asset(
            "Kia",
            "000270.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "POSCO Holdings": _asset(
            "POSCO Holdings",
            "005490.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "NAVER": _asset(
            "NAVER",
            "035420.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Kakao": _asset(
            "Kakao",
            "035720.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Celltrion": _asset(
            "Celltrion",
            "068270.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "LG Chem": _asset(
            "LG Chem",
            "051910.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Samsung SDI": _asset(
            "Samsung SDI",
            "006400.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "KB Financial": _asset(
            "KB Financial",
            "105560.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Shinhan Financial": _asset(
            "Shinhan Financial",
            "055550.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Hana Financial": _asset(
            "Hana Financial",
            "086790.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Samsung C&T": _asset(
            "Samsung C&T",
            "028260.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Hanwha Aerospace": _asset(
            "Hanwha Aerospace",
            "012450.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "HD Hyundai Heavy Industries": _asset(
            "HD Hyundai Heavy Industries",
            "329180.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "HD Korea Shipbuilding & Offshore Engineering": _asset(
            "HD Korea Shipbuilding & Offshore Engineering",
            "009540.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Doosan Enerbility": _asset(
            "Doosan Enerbility",
            "034020.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
    }
)

KOREA_STOCKS.update(
    {
        "SK Innovation": _asset(
            "SK Innovation",
            "096770.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Korea Electric Power": _asset(
            "Korea Electric Power",
            "015760.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Korean Air": _asset(
            "Korean Air",
            "003490.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "KT": _asset(
            "KT",
            "030200.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "LG Uplus": _asset(
            "LG Uplus",
            "032640.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Samsung Fire & Marine Insurance": _asset(
            "Samsung Fire & Marine Insurance",
            "000810.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Meritz Financial": _asset(
            "Meritz Financial",
            "138040.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Hyundai Mobis": _asset(
            "Hyundai Mobis",
            "012330.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Korea Zinc": _asset(
            "Korea Zinc",
            "010130.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Amorepacific": _asset(
            "Amorepacific",
            "090430.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Orion": _asset(
            "Orion",
            "271560.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Lotte Chemical": _asset(
            "Lotte Chemical",
            "011170.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "SK Square": _asset(
            "SK Square",
            "402340.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "CJ CheilJedang": _asset(
            "CJ CheilJedang",
            "097950.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "LG Electronics": _asset(
            "LG Electronics",
            "066570.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Samsung Electro-Mechanics": _asset(
            "Samsung Electro-Mechanics",
            "009150.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "SK Telecom": _asset(
            "SK Telecom",
            "017670.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Hyundai Glovis": _asset(
            "Hyundai Glovis",
            "086280.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "KakaoBank": _asset(
            "KakaoBank",
            "323410.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
        "Kakao Pay": _asset(
            "Kakao Pay",
            "377300.KS",
            CATEGORY_STOCK,
            MARKET_KOREA,
        ),
    }
)

# ==========================================================
# USA Stocks
# ==========================================================

US_STOCKS.update(
    {
        "Apple": _asset(
            "Apple",
            "AAPL",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Microsoft": _asset(
            "Microsoft",
            "MSFT",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "NVIDIA": _asset(
            "NVIDIA",
            "NVDA",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Amazon": _asset(
            "Amazon",
            "AMZN",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Alphabet Class A": _asset(
            "Alphabet Class A",
            "GOOGL",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Alphabet Class C": _asset(
            "Alphabet Class C",
            "GOOG",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Meta Platforms": _asset(
            "Meta Platforms",
            "META",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Tesla": _asset(
            "Tesla",
            "TSLA",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Broadcom": _asset(
            "Broadcom",
            "AVGO",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "AMD": _asset(
            "Advanced Micro Devices",
            "AMD",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Oracle": _asset(
            "Oracle",
            "ORCL",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Netflix": _asset(
            "Netflix",
            "NFLX",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Palantir": _asset(
            "Palantir Technologies",
            "PLTR",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Salesforce": _asset(
            "Salesforce",
            "CRM",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Adobe": _asset(
            "Adobe",
            "ADBE",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Cisco": _asset(
            "Cisco Systems",
            "CSCO",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "IBM": _asset(
            "IBM",
            "IBM",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Qualcomm": _asset(
            "Qualcomm",
            "QCOM",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Intel": _asset(
            "Intel",
            "INTC",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Micron": _asset(
            "Micron Technology",
            "MU",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Applied Materials": _asset(
            "Applied Materials",
            "AMAT",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Lam Research": _asset(
            "Lam Research",
            "LRCX",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "KLA": _asset(
            "KLA",
            "KLAC",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "ASML Holding": _asset(
            "ASML Holding",
            "ASML",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
        "Texas Instruments": _asset(
            "Texas Instruments",
            "TXN",
            CATEGORY_STOCK,
            MARKET_USA,
        ),
    }
)

# ==========================================================
# Global Indices
# ==========================================================

GLOBAL_INDICES.update(
    {
        "KOSPI": _asset(
            "KOSPI",
            "^KS11",
            CATEGORY_INDEX,
            MARKET_KOREA,
        ),
        "KOSDAQ": _asset(
            "KOSDAQ",
            "^KQ11",
            CATEGORY_INDEX,
            MARKET_KOREA,
        ),
        "S&P 500": _asset(
            "S&P 500",
            "^GSPC",
            CATEGORY_INDEX,
            MARKET_USA,
        ),
        "NASDAQ Composite": _asset(
            "NASDAQ Composite",
            "^IXIC",
            CATEGORY_INDEX,
            MARKET_USA,
        ),
        "Dow Jones Industrial Average": _asset(
            "Dow Jones Industrial Average",
            "^DJI",
            CATEGORY_INDEX,
            MARKET_USA,
        ),
        "Russell 2000": _asset(
            "Russell 2000",
            "^RUT",
            CATEGORY_INDEX,
            MARKET_USA,
        ),
        "Nikkei 225": _asset(
            "Nikkei 225",
            "^N225",
            CATEGORY_INDEX,
            MARKET_JAPAN,
        ),
        "TOPIX": _asset(
            "TOPIX",
            "^TOPX",
            CATEGORY_INDEX,
            MARKET_JAPAN,
        ),
        "Hang Seng": _asset(
            "Hang Seng",
            "^HSI",
            CATEGORY_INDEX,
            MARKET_HONGKONG,
        ),
        "Shanghai Composite": _asset(
            "Shanghai Composite",
            "000001.SS",
            CATEGORY_INDEX,
            MARKET_CHINA,
        ),
        "Shenzhen Component": _asset(
            "Shenzhen Component",
            "399001.SZ",
            CATEGORY_INDEX,
            MARKET_CHINA,
        ),
        "Taiwan Weighted": _asset(
            "Taiwan Weighted",
            "^TWII",
            CATEGORY_INDEX,
            MARKET_TAIWAN,
        ),
        "DAX": _asset(
            "DAX",
            "^GDAXI",
            CATEGORY_INDEX,
            MARKET_GERMANY,
        ),
        "CAC 40": _asset(
            "CAC 40",
            "^FCHI",
            CATEGORY_INDEX,
            MARKET_FRANCE,
        ),
        "FTSE 100": _asset(
            "FTSE 100",
            "^FTSE",
            CATEGORY_INDEX,
            MARKET_UK,
        ),
        "NIFTY 50": _asset(
            "NIFTY 50",
            "^NSEI",
            CATEGORY_INDEX,
            MARKET_INDIA,
        ),
    }
)


# ==========================================================
# ETFs
# ==========================================================

ETFS.update(
    {
        "SPY": _asset(
            "SPY",
            "SPY",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "VOO": _asset(
            "VOO",
            "VOO",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "IVV": _asset(
            "IVV",
            "IVV",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "QQQ": _asset(
            "QQQ",
            "QQQ",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "VTI": _asset(
            "VTI",
            "VTI",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "SCHD": _asset(
            "SCHD",
            "SCHD",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "VYM": _asset(
            "VYM",
            "VYM",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "XLK": _asset(
            "XLK",
            "XLK",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "XLF": _asset(
            "XLF",
            "XLF",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "XLE": _asset(
            "XLE",
            "XLE",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "SOXX": _asset(
            "SOXX",
            "SOXX",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "SMH": _asset(
            "SMH",
            "SMH",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "GLD": _asset(
            "GLD",
            "GLD",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "SLV": _asset(
            "SLV",
            "SLV",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "TLT": _asset(
            "TLT",
            "TLT",
            CATEGORY_ETF,
            MARKET_USA,
        ),
        "IWM": _asset(
            "IWM",
            "IWM",
            CATEGORY_ETF,
            MARKET_USA,
        ),
    }
)

# ==========================================================
# Foreign Exchange (FX)
# ==========================================================

FX.update(
    {
        "USD/KRW": _asset(
            "USD/KRW",
            "KRW=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "USD/JPY": _asset(
            "USD/JPY",
            "JPY=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "EUR/USD": _asset(
            "EUR/USD",
            "EURUSD=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "GBP/USD": _asset(
            "GBP/USD",
            "GBPUSD=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "AUD/USD": _asset(
            "AUD/USD",
            "AUDUSD=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "USD/CNY": _asset(
            "USD/CNY",
            "CNY=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "USD/CHF": _asset(
            "USD/CHF",
            "CHF=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "USD/CAD": _asset(
            "USD/CAD",
            "CAD=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "EUR/JPY": _asset(
            "EUR/JPY",
            "EURJPY=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
        "EUR/GBP": _asset(
            "EUR/GBP",
            "EURGBP=X",
            CATEGORY_FX,
            MARKET_GLOBAL,
        ),
    }
)


# ==========================================================
# Commodities
# ==========================================================

COMMODITIES.update(
    {
        "Gold": _asset(
            "Gold",
            "GC=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Silver": _asset(
            "Silver",
            "SI=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Copper": _asset(
            "Copper",
            "HG=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "WTI Crude Oil": _asset(
            "WTI Crude Oil",
            "CL=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Brent Crude Oil": _asset(
            "Brent Crude Oil",
            "BZ=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Natural Gas": _asset(
            "Natural Gas",
            "NG=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Corn": _asset(
            "Corn",
            "ZC=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Soybeans": _asset(
            "Soybeans",
            "ZS=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Coffee": _asset(
            "Coffee",
            "KC=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
        "Sugar": _asset(
            "Sugar",
            "SB=F",
            CATEGORY_COMMODITY,
            MARKET_GLOBAL,
        ),
    }
)


# ==========================================================
# Bonds
# ==========================================================

BONDS.update(
    {
        "US 2Y Treasury": _asset(
            "US 2Y Treasury",
            "^IRX",
            CATEGORY_BOND,
            MARKET_USA,
        ),
        "US 5Y Treasury": _asset(
            "US 5Y Treasury",
            "^FVX",
            CATEGORY_BOND,
            MARKET_USA,
        ),
        "US 10Y Treasury": _asset(
            "US 10Y Treasury",
            "^TNX",
            CATEGORY_BOND,
            MARKET_USA,
        ),
        "US 30Y Treasury": _asset(
            "US 30Y Treasury",
            "^TYX",
            CATEGORY_BOND,
            MARKET_USA,
        ),
    }
)

# ==========================================================
# Crypto
# ==========================================================

CRYPTO.update(
    {
        "Bitcoin": _asset(
            "Bitcoin",
            "BTC-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Ethereum": _asset(
            "Ethereum",
            "ETH-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "BNB": _asset(
            "BNB",
            "BNB-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Solana": _asset(
            "Solana",
            "SOL-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "XRP": _asset(
            "XRP",
            "XRP-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Dogecoin": _asset(
            "Dogecoin",
            "DOGE-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Cardano": _asset(
            "Cardano",
            "ADA-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Avalanche": _asset(
            "Avalanche",
            "AVAX-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "TRON": _asset(
            "TRON",
            "TRX-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Chainlink": _asset(
            "Chainlink",
            "LINK-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Polkadot": _asset(
            "Polkadot",
            "DOT-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Litecoin": _asset(
            "Litecoin",
            "LTC-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Bitcoin Cash": _asset(
            "Bitcoin Cash",
            "BCH-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Stellar": _asset(
            "Stellar",
            "XLM-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Toncoin": _asset(
            "Toncoin",
            "TON11419-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Sui": _asset(
            "Sui",
            "SUI20947-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Aptos": _asset(
            "Aptos",
            "APT21794-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Near Protocol": _asset(
            "Near Protocol",
            "NEAR-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Internet Computer": _asset(
            "Internet Computer",
            "ICP-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
        "Render": _asset(
            "Render",
            "RENDER-USD",
            CATEGORY_CRYPTO,
            MARKET_GLOBAL,
        ),
    }
)

# ==========================================================
# Asset Universe
# ==========================================================

ALL_ASSETS: Dict[str, Asset] = (
    KOREA_STOCKS
    | US_STOCKS
    | GLOBAL_INDICES
    | ETFS
    | FX
    | COMMODITIES
    | BONDS
    | CRYPTO
)


# ==========================================================
# Lookup Tables
# ==========================================================

ASSET_BY_TICKER: Dict[str, Asset] = {
    asset.ticker: asset
    for asset in ALL_ASSETS.values()
}

ASSET_NAMES: List[str] = sorted(
    ALL_ASSETS.keys()
)

MARKETS: List[str] = sorted(
    {
        asset.market
        for asset in ALL_ASSETS.values()
    }
)

CATEGORIES: List[str] = sorted(
    {
        asset.category
        for asset in ALL_ASSETS.values()
    }
)


# ==========================================================
# Market Maps
# ==========================================================

MARKET_MAP: Dict[str, Dict[str, Asset]] = {}

for asset_name, asset in ALL_ASSETS.items():

    MARKET_MAP.setdefault(
        asset.market,
        {}
    )

    MARKET_MAP[asset.market][asset_name] = asset


CATEGORY_MAP: Dict[str, Dict[str, Asset]] = {}

for asset_name, asset in ALL_ASSETS.items():

    CATEGORY_MAP.setdefault(
        asset.category,
        {}
    )

    CATEGORY_MAP[asset.category][asset_name] = asset


MARKET_CATEGORY_MAP: Dict[
    tuple[str, str],
    Dict[str, Asset],
] = {}

for asset_name, asset in ALL_ASSETS.items():

    key = (
        asset.market,
        asset.category,
    )

    MARKET_CATEGORY_MAP.setdefault(
        key,
        {}
    )

    MARKET_CATEGORY_MAP[key][asset_name] = asset

# ==========================================================
# Public API
# ==========================================================

def get_asset(name: str) -> Asset:
    """
    Return an Asset by its display name.

    Raises
    ------
    KeyError
        If the asset does not exist.
    """
    return ALL_ASSETS[name]


def get_ticker(name: str) -> str:
    """
    Return the Yahoo Finance ticker.
    """
    return get_asset(name).ticker


def get_asset_names() -> list[str]:
    """
    Return all asset display names.
    """
    return ASSET_NAMES.copy()


def get_markets() -> list[str]:
    """
    Return all supported markets.
    """
    return MARKETS.copy()


def get_categories() -> list[str]:
    """
    Return all supported categories.
    """
    return CATEGORIES.copy()


def get_assets_by_market(
    market: str,
) -> dict[str, Asset]:
    """
    Return assets filtered by market.
    """
    return MARKET_MAP.get(
        market,
        {},
    ).copy()


def get_assets_by_category(
    category: str,
) -> dict[str, Asset]:
    """
    Return assets filtered by category.
    """
    return CATEGORY_MAP.get(
        category,
        {},
    ).copy()


def get_assets_by_market_and_category(
    market: str,
    category: str,
) -> dict[str, Asset]:
    """
    Return assets filtered by both market and category.
    """
    return MARKET_CATEGORY_MAP.get(
        (market, category),
        {},
    ).copy()


def get_asset_by_ticker(
    ticker: str,
) -> Asset | None:
    """
    Return an Asset from a Yahoo Finance ticker.

    Returns
    -------
    Asset | None
    """
    return ASSET_BY_TICKER.get(ticker)


def search_assets(
    keyword: str,
) -> dict[str, Asset]:
    """
    Search assets by display name or ticker.

    Case-insensitive.
    """
    keyword = keyword.lower().strip()

    if not keyword:
        return {}

    return {
        name: asset
        for name, asset in ALL_ASSETS.items()
        if (
            keyword in name.lower()
            or keyword in asset.ticker.lower()
        )
    }


def has_asset(
    name: str,
) -> bool:
    """
    Check whether an asset exists.
    """
    return name in ALL_ASSETS


def has_ticker(
    ticker: str,
) -> bool:
    """
    Check whether a ticker exists.
    """
    return ticker in ASSET_BY_TICKER

# ==========================================================
# Validation
# ==========================================================

def validate_asset_universe() -> None:
    """
    Validate the internal consistency of the asset universe.

    Raises
    ------
    ValueError
        If duplicate tickers are found.
    """

    tickers = [asset.ticker for asset in ALL_ASSETS.values()]

    duplicated = {
        ticker
        for ticker in tickers
        if tickers.count(ticker) > 1
    }

    if duplicated:
        raise ValueError(
            f"Duplicate Yahoo Finance tickers found: "
            f"{sorted(duplicated)}"
        )


# Validate at import time.
validate_asset_universe()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    # Model
    "Asset",

    # Asset Groups
    "KOREA_STOCKS",
    "US_STOCKS",
    "GLOBAL_INDICES",
    "ETFS",
    "FX",
    "COMMODITIES",
    "BONDS",
    "CRYPTO",
    "ALL_ASSETS",

    # Lookup Tables
    "ASSET_BY_TICKER",
    "ASSET_NAMES",
    "MARKETS",
    "CATEGORIES",
    "MARKET_MAP",
    "CATEGORY_MAP",
    "MARKET_CATEGORY_MAP",

    # Public API
    "get_asset",
    "get_ticker",
    "get_asset_names",
    "get_markets",
    "get_categories",
    "get_assets_by_market",
    "get_assets_by_category",
    "get_assets_by_market_and_category",
    "get_asset_by_ticker",
    "search_assets",
    "has_asset",
    "has_ticker",

    # Validation
    "validate_asset_universe",
]
