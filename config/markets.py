"""Market and asset definitions using Enum for scalability."""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class MarketEnum(str, Enum):
    """Supported global markets.
    
    Allows easy addition of new markets with minimal code changes.
    """
    
    KOREA = "KR"
    USA = "US"
    JAPAN = "JP"
    HONG_KONG = "HK"
    CHINA = "CN"
    TAIWAN = "TW"
    UNITED_KINGDOM = "GB"
    GERMANY = "DE"
    FRANCE = "FR"
    
    def __str__(self) -> str:
        """Return market name."""
        market_names = {
            "KR": "Korea",
            "US": "USA",
            "JP": "Japan",
            "HK": "Hong Kong",
            "CN": "China",
            "TW": "Taiwan",
            "GB": "United Kingdom",
            "DE": "Germany",
            "FR": "France",
        }
        return market_names.get(self.value, self.value)
    
    def get_display_name(self) -> str:
        """Get human-readable market name."""
        return str(self)


class AssetTypeEnum(str, Enum):
    """Supported asset types."""
    
    STOCK = "stock"
    ETF = "etf"
    BOND = "bond"
    FX = "fx"
    COMMODITY = "commodity"
    CRYPTO = "crypto"


@dataclass
class Market:
    """Market information container.
    
    Attributes:
        code: Market code (e.g., 'KR', 'US').
        name: Human-readable market name.
        currency: Primary currency for the market.
        timezone: Market timezone.
        trading_hours: Market trading hours (optional).
        data_sources: List of available data sources.
    """
    
    code: str
    name: str
    currency: str
    timezone: str
    trading_hours: Optional[str] = None
    data_sources: List[str] = None
    
    def __post_init__(self):
        """Initialize data sources."""
        if self.data_sources is None:
            self.data_sources = ["yahoo", "fred"]


# Market registry for easy lookup and management
MARKET_REGISTRY: Dict[MarketEnum, Market] = {
    MarketEnum.KOREA: Market(
        code="KR",
        name="Korea",
        currency="KRW",
        timezone="Asia/Seoul",
        trading_hours="09:00-15:30",
        data_sources=["krx", "ecos", "yahoo"]
    ),
    MarketEnum.USA: Market(
        code="US",
        name="USA",
        currency="USD",
        timezone="America/New_York",
        trading_hours="09:30-16:00",
        data_sources=["yahoo", "fred"]
    ),
    MarketEnum.JAPAN: Market(
        code="JP",
        name="Japan",
        currency="JPY",
        timezone="Asia/Tokyo",
        trading_hours="09:00-15:00",
        data_sources=["yahoo"]
    ),
    MarketEnum.HONG_KONG: Market(
        code="HK",
        name="Hong Kong",
        currency="HKD",
        timezone="Asia/Hong_Kong",
        trading_hours="09:30-16:00",
        data_sources=["yahoo"]
    ),
    MarketEnum.CHINA: Market(
        code="CN",
        name="China",
        currency="CNY",
        timezone="Asia/Shanghai",
        trading_hours="09:30-15:00",
        data_sources=["yahoo"]
    ),
    MarketEnum.TAIWAN: Market(
        code="TW",
        name="Taiwan",
        currency="TWD",
        timezone="Asia/Taipei",
        trading_hours="09:00-13:30",
        data_sources=["yahoo"]
    ),
    MarketEnum.UNITED_KINGDOM: Market(
        code="GB",
        name="United Kingdom",
        currency="GBP",
        timezone="Europe/London",
        trading_hours="08:00-16:30",
        data_sources=["yahoo", "fred"]
    ),
    MarketEnum.GERMANY: Market(
        code="DE",
        name="Germany",
        currency="EUR",
        timezone="Europe/Berlin",
        trading_hours="08:00-20:00",
        data_sources=["yahoo"]
    ),
    MarketEnum.FRANCE: Market(
        code="FR",
        name="France",
        currency="EUR",
        timezone="Europe/Paris",
        trading_hours="08:00-20:00",
        data_sources=["yahoo"]
    ),
}


def get_market(market_enum: MarketEnum) -> Market:
    """Get market information by enum.
    
    Args:
        market_enum: MarketEnum value.
        
    Returns:
        Market object.
        
    Raises:
        ValueError: If market not found.
    """
    if market_enum not in MARKET_REGISTRY:
        raise ValueError(f"Market {market_enum} not supported")
    return MARKET_REGISTRY[market_enum]


def get_all_markets() -> Dict[MarketEnum, Market]:
    """Get all supported markets.
    
    Returns:
        Dictionary of all markets.
    """
    return MARKET_REGISTRY.copy()
