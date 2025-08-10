import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(backtest_results: pd.DataFrame, ticker: str):
    df = backtest_results[backtest_results['Ticker'] == ticker]
    plt.figure(figsize=(10, 4))
    plt.plot(df['Date'], df['Equity'], label='Equity Curve')
    plt.title(f'Equity Curve for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.legend()
    plt.tight_layout()
    plt.show()
