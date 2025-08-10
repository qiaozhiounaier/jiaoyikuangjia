class RiskManager:
    """Simple risk manager that stores max capital allocation per ticker."""
    def __init__(self, max_allocation: dict[str, float]):
        self.max_allocation = max_allocation

    def get_allocation(self, ticker: str) -> float:
        return self.max_allocation.get(ticker, 0.0)
