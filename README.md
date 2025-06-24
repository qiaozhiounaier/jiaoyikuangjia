# Trading Framework

This repository provides a minimal multi-asset trading framework suitable for institutional-style experimentation. It supports automated data acquisition, strategy implementation, backtesting, and result visualization.

## Features

- Fetch historical price data using `yfinance` or local CSV files.
- Define trading strategies using a clear class-based structure.
- Run vectorized backtests with capital tracking.
- Plot equity curves for individual tickers.

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
from trading_framework.backtest.backtester import Backtester
from trading_framework.visualization.plot_results import plot_equity_curve

provider = DataProvider(source="local")
data = provider.get_price_data(["AAPL", "GOOG"], "2024-01-01", "2024-01-05")
strategy = MovingAverageCrossStrategy(short=2, long=3)
signals = strategy.generate_signals(data)
backtester = Backtester(data, signals)
results = backtester.run()
plot_equity_curve(results, "AAPL")
```
