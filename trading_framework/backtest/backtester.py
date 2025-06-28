import pandas as pd
from ..risk.risk_manager import RiskManager
from ..execution.execution_engine import ExecutionEngine

class Backtester:
    def __init__(self, data: pd.DataFrame, signals: pd.DataFrame, capital: float = 100000.0,
                 risk_manager: RiskManager | None = None, execution_engine: ExecutionEngine | None = None):
        self.data = data
        self.signals = signals
        self.capital = capital
        self.risk_manager = risk_manager or RiskManager({})
        self.execution_engine = execution_engine or ExecutionEngine()

    def run(self) -> pd.DataFrame:
        merged = pd.merge(self.data, self.signals, on=["Date", "Ticker"])
        merged = merged.sort_values(["Date", "Ticker"])

        merged["Position"] = merged.groupby("Ticker")["Signal"].shift().fillna(0)
        merged["Trade"] = merged.groupby("Ticker")["Signal"].diff().abs().fillna(merged["Signal"].abs())
        merged["Market_Return"] = merged.groupby("Ticker")["Close"].pct_change()
        merged["Strategy_Return"] = merged["Market_Return"] * merged["Position"]
        merged["Strategy_Return"] -= merged["Trade"] * self.execution_engine.slippage

        n = merged["Ticker"].nunique()
        allocations = {t: self.capital / n for t in merged["Ticker"].unique()}
        for t, alloc in self.risk_manager.max_allocation.items():
            allocations[t] = self.capital * alloc
        merged["Allocation"] = merged["Ticker"].map(allocations)
        merged["Trade_Cost"] = merged["Trade"] * self.execution_engine.commission
        merged["Equity"] = (
            (1 + merged.groupby("Ticker")["Strategy_Return"].cumprod().fillna(1))
            * merged["Allocation"]
            - merged.groupby("Ticker")["Trade_Cost"].cumsum()
        )
        merged["Portfolio_Equity"] = merged.groupby("Date")["Equity"].transform("sum")
        return merged
