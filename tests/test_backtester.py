import pandas as pd
from trading_framework.data.data_provider import DataProvider
from trading_framework.strategy.moving_average import MovingAverageCrossStrategy
from trading_framework.backtest.backtester import Backtester


def test_backtest_runs():
    provider = DataProvider(source="local")
    data = provider.get_price_data(["AAPL", "GOOG"], start="2024-01-01", end="2024-01-05")
    strat = MovingAverageCrossStrategy(short=2, long=3)
    signals = strat.generate_signals(data)
    backtester = Backtester(data, signals)
    results = backtester.run()
    assert not results.empty
    assert "Equity" in results.columns
