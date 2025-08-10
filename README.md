# Trading Framework

This repository provides a minimal multi-asset trading framework suitable for institutional-style experimentation. It supports automated data acquisition, strategy implementation, backtesting, and result visualization.

The design is inspired by the structure of the [Chan](https://github.com/nextang/Chan) project and focuses on easily extending to multiple instruments.

## Features

- Fetch historical price data using `yfinance` or local CSV files with caching to speed up repeated runs.
- Define trading strategies using a clear class-based structure.
- Run vectorized backtests with capital tracking and automatic portfolio aggregation.
- Plot equity curves for individual tickers.
- Enforce capital allocation limits with a flexible `RiskManager`.
- Simulate slippage and commissions via an `ExecutionEngine`.

## Quickstart

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Example usage:

```python
from trading_framework.data.data_provider import DataProvider
from trading_framework.strategy.moving_average import MovingAverageCrossStrategy
from trading_framework.risk.risk_manager import RiskManager
from trading_framework.execution.execution_engine import ExecutionEngine
from trading_framework.backtest.backtester import Backtester
from trading_framework.visualization.plot_results import plot_equity_curve

provider = DataProvider()
data = provider.get_price_data(["AAPL", "GOOG"], "2024-01-01", "2024-01-05")
strategy = MovingAverageCrossStrategy(short=2, long=3)
signals = strategy.generate_signals(data)
risk = RiskManager({"AAPL": 0.6, "GOOG": 0.4})
engine = ExecutionEngine(slippage=0.001, commission=1)
backtester = Backtester(data, signals, risk_manager=risk, execution_engine=engine)
results = backtester.run()
plot_equity_curve(results, "AAPL")
print(results[["Date", "Portfolio_Equity"]].drop_duplicates().tail())
```
