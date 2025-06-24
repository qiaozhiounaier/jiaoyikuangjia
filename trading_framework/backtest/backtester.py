import pandas as pd
from typing import Callable

class Backtester:
    def __init__(self, data: pd.DataFrame, signals: pd.DataFrame, capital: float = 100000.0):
        self.data = data
        self.signals = signals
        self.capital = capital

    def run(self) -> pd.DataFrame:
        merged = pd.merge(self.data, self.signals, on=['Date', 'Ticker'])
        merged = merged.sort_values(['Date', 'Ticker'])
        merged['Position'] = merged['Signal'].shift()
        merged['Position'].fillna(0, inplace=True)
        merged['Market_Return'] = merged['Close'].pct_change()
        merged['Strategy_Return'] = merged['Market_Return'] * merged['Position']
        merged['Equity'] = (1 + merged['Strategy_Return']).cumprod() * self.capital
        return merged
