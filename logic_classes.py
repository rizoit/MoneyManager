from descriptors import *


class Transaction:
    id = IntValidator()
    transaction_date = DateTimeValidator()
    amount = FloatValidator()
    wallet_id = IntValidator()
    description = StringValidator(200)

    def __init__(self, id, transaction_date, amount, wallet_id, description=None):
        self.id = id
        self.transaction_date = transaction_date
        self.amount = amount
        self.wallet_id = wallet_id
        self.description = description

class Income(Transaction):

    category = "income"
    transaction_type = CategoryValidator()
    def __init__(self, id, transaction_date, amount, wallet_id, description, transaction_type):
        super().__init__(id, transaction_date, amount, wallet_id, description)
        self.transaction_type = transaction_type

    def __repr__(self):
        return f'Income: (id: {self.id}, date: {self.transaction_date}, amount: {self.amount}, ' \
               f'wallet_id: {self.wallet_id}, desc: {self.description}, type: {self.transaction_type})'

class Expense(Transaction):

    category = "expense"
    transaction_type = CategoryValidator()
    def __init__(self, id, transaction_date, amount, wallet_id, description, transaction_type):
        super().__init__(id, transaction_date, amount, wallet_id, description)
        self.transaction_type = transaction_type

    def __repr__(self):
        return f'Expense: (id: {self.id}, date: {self.transaction_date}, amount: {self.amount}, ' \
               f'wallet_id: {self.wallet_id}, desc: {self.description}, type: {self.transaction_type})'


class Wallet:
    wallet_name = StringValidator(25)
    initial_amount = FloatValidator()
    wallet_id = IntValidator()

    def __init__(self, wallet_id, wallet_name, wallet_type, initial_amount):
        self.wallet_id = wallet_id
        self.wallet_name = wallet_name
        self.wallet_type = wallet_type
        self.initial_amount = initial_amount
        self.transaction_history = set()


class Account:
    account_name = StringValidator(25)

    def __init__(self, account_name):
        self.account_name = account_name
        self.wallet_set = set()
