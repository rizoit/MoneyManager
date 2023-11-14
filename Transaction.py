from abc import abstractmethod
from datetime import datetime


class Transaction:
    """
    Represents a single transaction.
    """
    def __init__(self, date:datetime, amount:float, account_name:str, currency:str = 'USD', fee:float = 0, category = None):

        self.date: datetime.date = date
        self.amount: float = amount
        self.account_name: str = account_name
        self.fee: float = fee
        self.category: str = category
        self.currency: str = currency
    @abstractmethod
    def __repr__(self):
        pass

class Deposit(Transaction):
    """
    Represents a single transaction for depositing funds.
    """
    def __init__(self, date, amount, account_name, currency = 'USD', fee = 0):
        super().__init__(date, amount, account_name, currency, fee)
        self.category = 'Deposit'

    def __repr__(self):
        return f"Deposit(date={self.date}, amount={self.amount}, account_name={self.account_name}, currency={self.currency}, fee={self.fee})"

class Withdrawal(Transaction):
    """
    Represents a single transaction for withdrawing funds.
    """
    def __init__(self, date, amount, account_name, currency = 'USD', fee = 0):
        super().__init__(date, amount, account_name, currency, fee)
        self.category = 'Withdrawal'

    def __repr__(self):
        return f"Withdrawal(date={self.date}, amount={self.amount}, account_name={self.account_name}, currency={self.currency}, fee={self.fee})"
    
class BuyAsset(Transaction):
    """
    Represents a single transaction for buying an asset.
    """
    def __init__(self, date, ticker, number, amount, account_name, currency = 'USD', fee = 0):
        super().__init__(date, amount, account_name, currency, fee)
        self.ticker: str = ticker
        self.number: float = number

    def __repr__(self):
        return f"BuyAsset(date={self.date}, ticker={self.ticker}, number={self.number}, amount={self.amount}, account_name={self.account_name}, currency={self.currency}, fee={self.fee})"

class SellAsset(Transaction):
    """
    Represents a single transaction for selling an asset.
    """
    def __init__(self, date, ticker, number, amount, account_name, currency = 'USD', fee = 0):
        super().__init__(date, amount, account_name, currency, fee)
        self.ticker: str = ticker
        self.number: float = number

    def __repr__(self):
        return f"SellAsset(date={self.date}, ticker={self.ticker}, number={self.number}, amount={self.amount}, account_name={self.account_name}, currency={self.currency}, fee={self.fee})"
    
class Income(Transaction):
    """
    Represents a single transaction for income.
    """
    def __init__(self, date, amount, account_name, currency = 'USD', fee = 0, category = None):
        super().__init__(date, amount, account_name, currency, fee)
        self.category = category

    def __repr__(self):
        return f"Income(date={self.date}, amount={self.amount}, account_name={self.account_name}, currency={self.currency}, fee={self.fee}, category={self.category})"
    
class Dividend(Transaction):
    """
    Represents a single transaction for dividends.
    """
    def __init__(self, date, amount, account_name, currency = 'USD', fee = 0, ticker = None, witholding = None):
        super().__init__(date, amount, account_name, currency, fee)
        self.ticker: str = ticker
        self.witholding: float = witholding
        self.net_dividend: float = amount - witholding  

    def __repr__(self):
        return f"Dividend: {self.amount}, {self.date}, {self.account_name}"