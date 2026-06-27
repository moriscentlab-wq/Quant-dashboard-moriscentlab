"""
MQD Dashboard
Yahoo Finance Data Collector

실시간 시세를 Yahoo Finance에서 수집한다.
"""

from datetime import datetime

import pandas as pd
import yfinance as yf


def get_history(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Yahoo Finance에서 과거 데이터를 가져온다.

    Parameters
    ----------
    ticker : str
        Yahoo Finance 티커
    period : str
        ex) 1mo,3mo,6mo,1y,2y
    interval : str
        ex) 1d,1wk

    Returns
    -------
    pandas.DataFrame
    """

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
        threads=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    df = df.reset_index()

    return df


def get_latest_price(ticker: str) -> dict:
    """
    현재 가격 정보 반환
    """

    history = get_history(ticker, period="5d")

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    change = latest["Close"] - previous["Close"]
    change_pct = change / previous["Close"] * 100

    return {
        "ticker": ticker,
        "date": latest["Date"],
        "close": float(latest["Close"]),
        "change": float(change),
        "change_pct": float(change_pct),
        "volume": int(latest["Volume"]),
    }


def get_last_update() -> str:
    """
    Dashboard 업데이트 시간
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")