import os
from typing import List
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # fallback if yfinance not installed
    yf = None

class DataProvider:
    """Fetches historical price data for multiple tickers."""

    def __init__(self, source: str = "yfinance"):
        self.source = source

    def get_price_data(self, tickers: List[str], start: str, end: str) -> pd.DataFrame:
        if self.source == "yfinance" and yf is not None:
            df = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df = df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
            return df
        else:
            # fallback to local csv named <ticker>.csv
            frames = []
            for ticker in tickers:
                file_path = os.path.join(os.path.dirname(__file__), f"{ticker}.csv")
                if os.path.exists(file_path):
                    temp = pd.read_csv(file_path, parse_dates=['Date'])
                    temp['Ticker'] = ticker
                    frames.append(temp)
            if frames:
                return pd.concat(frames)
            raise RuntimeError('No data source available')
