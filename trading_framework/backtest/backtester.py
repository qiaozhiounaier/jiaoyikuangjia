import pandas as pd

class Backtester:
    def __init__(self, data: pd.DataFrame, signals: pd.DataFrame, capital: float = 100000.0):
        self.data = data
        self.signals = signals
        self.capital = capital

    def run(self) -> pd.DataFrame:
        merged = pd.merge(self.data, self.signals, on=["Date", "Ticker"])
        merged = merged.sort_values(["Date", "Ticker"])

        merged["Position"] = merged.groupby("Ticker")["Signal"].shift().fillna(0)
        merged["Market_Return"] = merged.groupby("Ticker")["Close"].pct_change()
        merged["Strategy_Return"] = merged["Market_Return"] * merged["Position"]

        capital_per_ticker = self.capital / merged["Ticker"].nunique()
        merged["Equity"] = (
            (1 + merged.groupby("Ticker")["Strategy_Return"].cumprod().fillna(1))
            * capital_per_ticker
        )
        merged["Portfolio_Equity"] = merged.groupby("Date")["Equity"].transform("sum")
        return merged
