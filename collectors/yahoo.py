"""
MQD Dashboard
Yahoo Finance Data Collector
"""

from datetime import datetime

import pandas as pd
import yfinance as yf


REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    yfinance 버전에 따라 MultiIndex가 반환되는 경우를 처리한다.
    """

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df


def get_history(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Yahoo Finance에서 과거 데이터를 가져온다.
    """

    try:

        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

    except Exception as exc:
        raise ConnectionError(
            f"Yahoo Finance download failed : {ticker}"
        ) from exc

    if df.empty:
        raise ValueError(f"No data returned : {ticker}")

    df = _normalize_columns(df)

    df = df.reset_index()

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            raise KeyError(f"Missing column : {column}")

    return df


def get_latest_price(ticker: str) -> dict:
    """
    최근 종가 및 변동률 반환
    """

    history = get_history(
        ticker=ticker,
        period="5d",
        interval="1d",
    )

    if len(history) < 2:
        raise ValueError(
            "Not enough historical data."
        )

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    change = latest["Close"] - previous["Close"]

    change_pct = (
        change / previous["Close"]
    ) * 100

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
    Dashboard 갱신 시각
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

def get_multiple_latest_prices(assets: dict) -> list[dict]:
    """
    여러 자산의 최신 가격 정보를 반환한다.
    """

    results = []

    for asset in assets.values():
        try:
            results.append(get_latest_price(asset.ticker))
        except Exception:
            continue

    return results