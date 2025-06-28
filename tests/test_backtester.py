import pandas as pd
from trading_framework.data.data_provider import DataProvider
from trading_framework.strategy.moving_average import MovingAverageCrossStrategy
from trading_framework.backtest.backtester import Backtester
from trading_framework.risk.risk_manager import RiskManager
from trading_framework.execution.execution_engine import ExecutionEngine


def test_backtest_runs():
    provider = DataProvider(source="local")
    data = provider.get_price_data(["AAPL", "GOOG"], start="2024-01-01", end="2024-01-05")
    strat = MovingAverageCrossStrategy(short=2, long=3)
    signals = strat.generate_signals(data)
    risk = RiskManager({"AAPL": 0.6, "GOOG": 0.4})
    engine = ExecutionEngine(slippage=0.0, commission=0.0)
    backtester = Backtester(data, signals, risk_manager=risk, execution_engine=engine)
    results = backtester.run()
    assert not results.empty
    assert "Equity" in results.columns
    assert "Portfolio_Equity" in results.columns


def test_data_provider_local():
    provider = DataProvider(source="local")
    data = provider.get_price_data(["AAPL"], start="2024-01-01", end="2024-01-05")
    assert not data.empty
    assert set(data["Ticker"]) == {"AAPL"}


def test_risk_manager_allocation():
    rm = RiskManager({"AAPL": 0.5})
    assert rm.get_allocation("AAPL") == 0.5
    assert rm.get_allocation("GOOG") == 0.0


def test_execution_engine_cost():
    engine = ExecutionEngine(slippage=0.01, commission=2)
    cost = engine.trade_cost(100, 10)
    assert cost == 100 * 1.01 * 10 + 2
