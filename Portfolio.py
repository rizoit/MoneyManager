class Portfolio:
    """
    Represents the entire portfolio.
    """
    def __init__(self):
        self.wallets = {}

    def add_wallet(self, wallet):
        """Adds a wallet to the portfolio."""
        self.wallets[wallet.name] = wallet

    def calculate_total_performance(self):
        """Calculates the overall performance of the portfolio."""
        total_performance = 0
        for wallet in self.wallets.values():
            total_performance += wallet.calculate_wallet_performance()
        return total_performance