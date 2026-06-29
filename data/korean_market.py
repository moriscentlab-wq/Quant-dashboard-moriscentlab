"""
Korean Market Universe

Mori Quant Investing
Research. Analyze. Decide.
"""

from dataclasses import dataclass


@dataclass
class Security:
    ticker: str
    name: str
    market: str


KOSPI = [
    Security("005930.KS", "삼성전자", "KOSPI"),
    Security("000660.KS", "SK하이닉스", "KOSPI"),
    Security("005380.KS", "현대차", "KOSPI"),
    Security("035420.KS", "NAVER", "KOSPI"),
    Security("051910.KS", "LG화학", "KOSPI"),
]


KOSDAQ = [
    Security("068270.KQ", "셀트리온", "KOSDAQ"),
    Security("247540.KQ", "에코프로비엠", "KOSDAQ"),
    Security("086520.KQ", "에코프로", "KOSDAQ"),
    Security("196170.KQ", "알테오젠", "KOSDAQ"),
    Security("357780.KQ", "솔브레인", "KOSDAQ"),
]


ETF = [
    Security("069500.KS", "KODEX200", "ETF"),
    Security("102110.KS", "TIGER200", "ETF"),
    Security("229200.KS", "KODEX 코스닥150", "ETF"),
    Security("114800.KS", "KODEX 인버스", "ETF"),
    Security("122630.KS", "KODEX 레버리지", "ETF"),
]


def get_market_universe(market: str):
    """Return securities for the selected market."""

    market = market.upper()

    if market == "KOSPI":
        return KOSPI

    if market == "KOSDAQ":
        return KOSDAQ

    if market == "ETF":
        return ETF

    return []
