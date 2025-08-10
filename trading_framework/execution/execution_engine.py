class ExecutionEngine:
    """Simulates trade execution with slippage and commissions."""
    def __init__(self, slippage: float = 0.0, commission: float = 0.0):
        self.slippage = slippage
        self.commission = commission

    def trade_cost(self, price: float, quantity: float) -> float:
        executed_price = price * (1 + self.slippage)
        return executed_price * quantity + self.commission
