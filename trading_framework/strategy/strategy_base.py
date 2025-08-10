import pandas as pd

class Strategy:
    """Base class for trading strategies."""

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return a DataFrame with at least 'Date', 'Ticker', and 'Signal' columns."""
        raise NotImplementedError
