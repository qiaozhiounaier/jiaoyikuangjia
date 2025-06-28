import os
from typing import List
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # fallback if yfinance not installed
    yf = None

class DataProvider:
    """Fetches historical price data for multiple tickers with optional caching."""

    def __init__(self, source: str = "yfinance", cache_dir: str | None = None):
        self.source = source
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), "cache")
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _cache_path(self, ticker: str) -> str:
        return os.path.join(self.cache_dir, f"{ticker}.csv")

    def _load_cached(self, ticker: str) -> pd.DataFrame | None:
        path = self._cache_path(ticker)
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Date"])
            df["Ticker"] = ticker
            return df
        return None

    def _save_cache(self, ticker: str, df: pd.DataFrame) -> None:
        df.to_csv(self._cache_path(ticker), index=False)

    def get_price_data(self, tickers: List[str], start: str, end: str) -> pd.DataFrame:
        frames = []
        for ticker in tickers:
            data = None
            if self.source == "yfinance" and yf is not None:
                try:
                    temp = yf.download(ticker, start=start, end=end, auto_adjust=True)
                    temp.reset_index(inplace=True)
                    temp["Ticker"] = ticker
                    data = temp
                    self._save_cache(ticker, temp)
                except Exception:
                    data = None
            if data is None:
                data = self._load_cached(ticker)
            if data is None and self.source == "local":
                file_path = os.path.join(os.path.dirname(__file__), f"{ticker}.csv")
                if os.path.exists(file_path):
                    data = pd.read_csv(file_path, parse_dates=["Date"])
                    data["Ticker"] = ticker
            if data is not None:
                frames.append(data)
        if frames:
            return pd.concat(frames)
        raise RuntimeError("No data source available")
