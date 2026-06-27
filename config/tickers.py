"""
MQD Dashboard
Yahoo Finance Ticker Configuration

모든 자산의 티커를 중앙에서 관리한다.
데이터 출처:
https://finance.yahoo.com
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Asset:
    name: str
    ticker: str


# ==========================
# Korea Index
# ==========================

KOREA = {
    "KOSPI": Asset("KOSPI", "^KS11"),
    "KOSDAQ": Asset("KOSDAQ", "^KQ11"),
    "KOSPI200": Asset("KOSPI200", "^KS200"),
    "KOSDAQ150": Asset("KOSDAQ150", "229200.KS"),
}


# ==========================
# USA Index
# ==========================

USA = {
    "S&P500": Asset("S&P500", "^GSPC"),
    "NASDAQ": Asset("NASDAQ", "^IXIC"),
    "Dow Jones": Asset("Dow Jones", "^DJI"),
    "Russell2000": Asset("Russell2000", "^RUT"),
    "NYSE Composite": Asset("NYSE Composite", "^NYA"),
    "AMEX Composite": Asset("AMEX Composite", "^XAX"),
}


# ==========================
# Korea ETF
# ==========================

KOREA_ETF = {
    "KODEX200": Asset("KODEX200", "069500.KS"),
    "TIGER200": Asset("TIGER200", "102110.KS"),
    "KODEXNASDAQ100": Asset("KODEXNASDAQ100", "379800.KS"),
    "TIGERS&P500": Asset("TIGERS&P500", "360750.KS"),
}


# ==========================
# USA ETF
# ==========================

USA_ETF = {
    "SPY": Asset("SPDR S&P500", "SPY"),
    "QQQ": Asset("Invesco QQQ", "QQQ"),
    "DIA": Asset("SPDR Dow", "DIA"),
    "IWM": Asset("Russell2000", "IWM"),
    "VTI": Asset("Vanguard Total Market", "VTI"),
    "VOO": Asset("Vanguard S&P500", "VOO"),
}


# ==========================
# FX
# ==========================

FX = {
    "USD/KRW": Asset("USD/KRW", "KRW=X"),
    "USD/JPY": Asset("USD/JPY", "JPY=X"),
    "USD/CNY": Asset("USD/CNY", "CNY=X"),
    "EUR/USD": Asset("EUR/USD", "EURUSD=X"),
    "DXY": Asset("US Dollar Index", "DX-Y.NYB"),
}


# ==========================
# Bond
# ==========================

BOND = {
    "US10Y": Asset("US 10Y Treasury", "^TNX"),
    "US30Y": Asset("US 30Y Treasury", "^TYX"),
    "US5Y": Asset("US 5Y Treasury", "^FVX"),
}


# ==========================
# Commodity
# ==========================

COMMODITY = {
    "Gold": Asset("Gold", "GC=F"),
    "Silver": Asset("Silver", "SI=F"),
    "Crude Oil": Asset("WTI Crude", "CL=F"),
    "Natural Gas": Asset("Natural Gas", "NG=F"),
    "Copper": Asset("Copper", "HG=F"),
}


# ==========================
# Crypto
# ==========================

CRYPTO = {
    "Bitcoin": Asset("Bitcoin", "BTC-USD"),
    "Ethereum": Asset("Ethereum", "ETH-USD"),
    "Solana": Asset("Solana", "SOL-USD"),
    "XRP": Asset("XRP", "XRP-USD"),
}


# ==========================
# All Assets
# ==========================

ALL_ASSETS: Dict[str, Dict[str, Asset]] = {
    "Korea": KOREA,
    "USA": USA,
    "Korea ETF": KOREA_ETF,
    "USA ETF": USA_ETF,
    "FX": FX,
    "Bond": BOND,
    "Commodity": COMMODITY,
    "Crypto": CRYPTO,
}