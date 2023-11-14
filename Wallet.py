from Asset import Asset


class Wallet:
    """
    Represents a wallet under a specific bank account.
    """
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.balance = initial_balance
        self.assets = {}
        self.transactions = []

    def add_asset(self, asset):
        """Adds an asset to the wallet."""
        self.assets[asset.ticker] = asset

    def process_transaction(self, transaction):
        """Processes a transaction and updates wallet balance and assets."""
        if transaction.order_type.lower() == "buy":
            cost = transaction.amount * transaction.price + transaction.fee
            if self.balance >= cost:
                self.balance -= cost
                if transaction.ticker not in self.assets:
                    self.assets[transaction.ticker] = Asset(transaction.ticker)
                self.assets[transaction.ticker].add_transaction(transaction)
            else:
                raise ValueError("Insufficient balance to complete the transaction.")
        elif transaction.order_type.lower() == "sell":
            if transaction.ticker in self.assets:
                revenue = transaction.amount * transaction.price - transaction.fee
                self.balance += revenue
                self.assets[transaction.ticker].add_transaction(transaction)
            else:
                raise ValueError(f"Asset {transaction.ticker} not found in wallet.")

    def calculate_wallet_performance(self):
        """Calculates the performance of the wallet."""
        wallet_performance = 0
        for asset in self.assets.values():
            wallet_performance += asset.calculate_return()
        return wallet_performance