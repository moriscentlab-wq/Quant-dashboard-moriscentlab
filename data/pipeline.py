```python
"""
Data Pipeline
Mori Quant Investing
"""

from typing import List
import pandas as pd

from data.korean_market import get_market_universe
from collectors.yahoo import get_history
from indicators.moving_average import calculate_moving_average
from indicators.rsi import calculate_rsi
from scoring.mqd_score import calculate_mqd_score


class DataPipeline:
    """Main data pipeline."""

    def load_market(self, market: str) -> pd.DataFrame:
        """Load market data."""

        rows: List[dict] = []

        securities = get_market_universe(market)

        for security in securities:

            try:
                history = get_history(security.ticker)

                history = calculate_moving_average(history)
                history = calculate_rsi(history)
                history = calculate_mqd_score(history)

                latest = history.iloc[-1]

                rows.append(
                    {
                        "Ticker": security.ticker,
                        "Company": security.name,
                        "Market": security.market,
                        "Price": latest["Close"],
                        "Volume": latest.get("Volume", 0),
                        "Trading Value": latest["Close"] * latest.get("Volume", 0),
                        "RSI": latest.get("RSI", 0),
                        "MQD Score": latest.get("MQD Score", 0),
                    }
                )

            except Exception:
                continue

        return pd.DataFrame(rows)

    def get_top_by_criterion(
        self,
        market: str,
        criterion: str = "Trading Value",
        top_n: int = 30,
    ) -> pd.DataFrame:
        """Return top securities by criterion."""

        df = self.load_market(market)

        if df.empty:
            return df

        if criterion not in df.columns:
            return df

        return (
            df.sort_values(
                by=criterion,
                ascending=False,
            )
            .head(top_n)
            .reset_index(drop=True)
        )

    def get_top30(self, market: str) -> pd.DataFrame:
        """Return Top30 by Trading Value."""

        return self.get_top_by_criterion(
            market=market,
            criterion="Trading Value",
            top_n=30,
        )

    def get_mqd_top10(self, market: str) -> pd.DataFrame:
        """Return Top10 by MQD Score."""

        df = self.load_market(market)

        if df.empty:
            return df

        return (
            df.sort_values(
                by="MQD Score",
                ascending=False,
            )
            .head(10)
            .reset_index(drop=True)
        )
```

