import pandas as pd
from .strategy_base import Strategy

class MovingAverageCrossStrategy(Strategy):
    def __init__(self, short: int = 10, long: int = 30):
        self.short = short
        self.long = long

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        results = []
        for ticker, group in data.groupby('Ticker'):
            df = group.sort_values('Date').copy()
            df['short_ma'] = df['Close'].rolling(self.short).mean()
            df['long_ma'] = df['Close'].rolling(self.long).mean()
            df['Signal'] = 0
            df.loc[df['short_ma'] > df['long_ma'], 'Signal'] = 1
            df.loc[df['short_ma'] < df['long_ma'], 'Signal'] = -1
            results.append(df[['Date', 'Ticker', 'Signal']])
        return pd.concat(results)
