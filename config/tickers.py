"""
Mori Quant Investing
Ticker Configuration
"""

from dataclasses import dataclass


@dataclass
class Asset:
    ticker: str
    name: str


ALL_ASSETS = {

    "KOSPI": {

        "삼성전자": Asset("005930.KS", "삼성전자"),
        "SK하이닉스": Asset("000660.KS", "SK하이닉스"),
        "현대차": Asset("005380.KS", "현대차"),
        "기아": Asset("000270.KS", "기아"),
        "NAVER": Asset("035420.KS", "NAVER"),
        "카카오": Asset("035720.KS", "카카오"),
        "LG에너지솔루션": Asset("373220.KS", "LG에너지솔루션"),
        "삼성바이오로직스": Asset("207940.KS", "삼성바이오로직스"),
        "POSCO홀딩스": Asset("005490.KS", "POSCO홀딩스"),
        "셀트리온": Asset("068270.KS", "셀트리온"),
        "KB금융": Asset("105560.KS", "KB금융"),
        "신한지주": Asset("055550.KS", "신한지주"),
        "하나금융지주": Asset("086790.KS", "하나금융지주"),
        "삼성물산": Asset("028260.KS", "삼성물산"),
        "LG화학": Asset("051910.KS", "LG화학"),
        "삼성SDI": Asset("006400.KS", "삼성SDI"),
        "한화에어로스페이스": Asset("012450.KS", "한화에어로스페이스"),
        "현대모비스": Asset("012330.KS", "현대모비스"),
        "SK이노베이션": Asset("096770.KS", "SK이노베이션"),
        "HD현대": Asset("267250.KS", "HD현대"),
    },

    "KOSDAQ": {

        "알테오젠": Asset("196170.KQ", "알테오젠"),
        "에코프로": Asset("086520.KQ", "에코프로"),
        "에코프로비엠": Asset("247540.KQ", "에코프로비엠"),
        "HLB": Asset("028300.KQ", "HLB"),
        "레인보우로보틱스": Asset("277810.KQ", "레인보우로보틱스"),
        "클래시스": Asset("214150.KQ", "클래시스"),
        "휴젤": Asset("145020.KQ", "휴젤"),
        "펄어비스": Asset("263750.KQ", "펄어비스"),
        "리노공업": Asset("058470.KQ", "리노공업"),
        "파마리서치": Asset("214450.KQ", "파마리서치"),
        "삼천당제약": Asset("000250.KQ", "삼천당제약"),
        "실리콘투": Asset("257720.KQ", "실리콘투"),
        "JYP": Asset("035900.KQ", "JYP"),
        "에스엠": Asset("041510.KQ", "에스엠"),
        "CJ ENM": Asset("035760.KQ", "CJ ENM"),
        "동진쎄미켐": Asset("005290.KQ", "동진쎄미켐"),
        "솔브레인": Asset("357780.KQ", "솔브레인"),
        "ISC": Asset("095340.KQ", "ISC"),
        "원익IPS": Asset("240810.KQ", "원익IPS"),
        "하나마이크론": Asset("067310.KQ", "하나마이크론"),
    },

    "ETF": {

        "KODEX200": Asset("069500.KS", "KODEX200"),
        "TIGER200": Asset("102110.KS", "TIGER200"),
        "KODEX 코스닥150": Asset("229200.KS", "KODEX 코스닥150"),
        "TIGER 미국S&P500": Asset("360750.KS", "TIGER 미국S&P500"),
        "TIGER 미국나스닥100": Asset("133690.KS", "TIGER 미국나스닥100"),
        "KODEX 레버리지": Asset("122630.KS", "KODEX 레버리지"),
        "KODEX 인버스": Asset("114800.KS", "KODEX 인버스"),
        "KODEX 반도체": Asset("091160.KS", "KODEX 반도체"),
        "TIGER 반도체": Asset("091230.KS", "TIGER 반도체"),
        "KODEX 은행": Asset("091170.KS", "KODEX 은행"),
        "KODEX 자동차": Asset("091180.KS", "KODEX 자동차"),
        "KODEX 2차전지산업": Asset("305720.KS", "KODEX 2차전지산업"),
        "KODEX 바이오": Asset("244580.KS", "KODEX 바이오"),
        "KODEX 헬스케어": Asset("266420.KS", "KODEX 헬스케어"),
        "KODEX 미국채10년": Asset("304660.KS", "KODEX 미국채10년"),
        "KODEX 골드선물": Asset("132030.KS", "KODEX 골드선물"),
        "TIGER 리츠": Asset("329200.KS", "TIGER 리츠"),
        "KODEX ESG": Asset("278530.KS", "KODEX ESG"),
        "KODEX BBIG": Asset("364980.KS", "KODEX BBIG"),
        "TIGER AI코리아그로스": Asset("463250.KS", "TIGER AI코리아그로스"),
    },
}
