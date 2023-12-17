from descriptors import *


class Transaction:
    id = IntValidator()
    transaction_date = DateTimeValidator()
    amount = FloatValidator()
    wallet_id_master = IntValidator()
    wallet_id_slave = IntValidator()
    description = StringValidator(200)

    def __init__(self, id, transaction_date, amount, wallet_id_master, wallet_id_slave=0, description=''):
        self.id = id
        self.transaction_date = transaction_date
        self.amount = amount
        self.wallet_id_master = wallet_id_master
        self.wallet_id_slave = wallet_id_slave
        self.description = description


class TransactionType:
    def __init__(self, transaction_type_id, category, transaction_type):
        self.category = category
        self.transaction_type = transaction_type
        self.transaction_type_id = transaction_type_id

    def __repr__(self):
        return f"TransactionType(id: {self.transaction_type_id}, category: {self.category}, transaction_type: {self.transaction_type})"


class Income(Transaction):
    transaction_type = CategoryValidator()

    def __init__(self, id, transaction_date, amount, wallet_id_master, wallet_id_slave, description, transaction_type):
        super().__init__(id, transaction_date, amount, wallet_id_master, wallet_id_slave, description)
        self.transaction_type = transaction_type

    def __repr__(self):
        return f'Income: (id: {self.id}, date: {self.transaction_date}, amount: {self.amount}, ' \
               f'wallet_id: {self.wallet_id_master}, desc: {self.description}, type: {self.transaction_type})'


class Expense(Transaction):
    category = "expense"
    transaction_type = CategoryValidator()

    def __init__(self, id, transaction_date, amount, wallet_id_master, wallet_id_slave, description, transaction_type):
        super().__init__(id, transaction_date, amount, wallet_id_master, wallet_id_slave, description)
        self.transaction_type = transaction_type

    def __repr__(self):
        return f'Expense: (id: {self.id}, date: {self.transaction_date}, amount: {self.amount}, ' \
               f'wallet_id: {self.wallet_id_master}, desc: {self.description}, type: {self.transaction_type})'


class Wallet:
    name = StringValidator(25)
    initial_amount = FloatValidator()
    wallet_id = IntValidator()

    def __init__(self, wallet_id, name, initial_amount):
        self.wallet_id = wallet_id
        self.name = name

        self.initial_amount = initial_amount
        self.transaction_history = list()

    def __repr__(self):
        return f"Wallet(wallet_id: {self.wallet_id}, wallet_name: {self.name}, initial_amount: {self.initial_amount})"




class Account:
    name = StringValidator(25)
    account_id = IntValidator()

    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name
        self.wallet_list = list()

    def add_wallet(self, wallet):
        if not isinstance(wallet, Wallet):
            raise TypeError(f"{wallet} is not instance of Wallet")
        self.wallet_list.append(wallet)

    def __repr__(self):
        return (f"Account(account_id: {self.account_id}, account_name: {self.name}, wallet_list: {self.wallet_list})")
