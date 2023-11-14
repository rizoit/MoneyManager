from asset_current_value import AssetCurrentValue


class Asset:
    """
    Represents a single asset in the portfolio.
    """
    def __init__(self, ticker, asset_type="stock" ):

        self.ticker = ticker
        self.asset_type = asset_type  # e.g., "stock", "cash", "interest"
        self.price = AssetCurrentValue(ticker).get_current_price()
        self.amount = 0
        self.value = 0
        self.average_cost = 0
        self.percentage = 0
        self.daily_performance = 0
        self.monthly_performance = 0
        self.yearly_performance = 0
        self.transactions = []  # List of transactions

    def add_transaction(self, transaction):
        """Adds a buy/sell transaction."""
        self.transactions.append(transaction)
        if transaction.order_type.lower() == "buy":
            total_cost = self.average_cost * self.amount + transaction.price * transaction.amount
            self.amount += transaction.amount
            self.average_cost = total_cost / self.amount
        elif transaction.order_type.lower() == "sell":
            self.amount -= transaction.amount
        self.value = self.price * self.amount

    def update_price(self, new_price):
        """Updates the current price of the asset."""
        self.price = new_price
        self.value = self.price * self.amount

    def calculate_return(self):
        """
        Calculates the return for the asset.
        """
        return (self.price - self.average_cost) * self.amount

    def calculate_sell_performance(self, sell_price, sell_amount):
        """
        Calculates profit or loss based on FIFO principle when selling an asset.
        """
        remaining_amount = sell_amount
        profit_or_loss = 0
        fifo_queue = []  # To store the buy transactions in FIFO order

        for transaction in self.transactions:
            if transaction.order_type.lower() == "buy":
                fifo_queue.append(transaction)

        while remaining_amount > 0 and fifo_queue:
            buy_transaction = fifo_queue.pop(0)
            if buy_transaction.amount <= remaining_amount:
                profit_or_loss += (sell_price - buy_transaction.price) * buy_transaction.amount
                remaining_amount -= buy_transaction.amount
            else:
                profit_or_loss += (sell_price - buy_transaction.price) * remaining_amount
                buy_transaction.amount -= remaining_amount
                fifo_queue.insert(0, buy_transaction)
                remaining_amount = 0

        return profit_or_loss