from abc import abstractmethod

from Transaction import SellAsset

import pdfplumber as pdfplumber
from datetime import datetime

from Transaction import BuyAsset, SellAsset, Deposit, Withdrawal, Income, Dividend


class ExtraitReader:
    """
    Abstract class representing a reader for extrait data.
    """

    @abstractmethod
    def read_excrait_data(self):
        pass


class ReadMidas(ExtraitReader):
    """
    Reader for extrait data from Midas.
    """
    def __init__(self):
        super().__init__()
        self.account_name = 'Midas'

    def read_excrait_data(self, file_path:str):
        transaction_history = []

        with pdfplumber.open(file_path) as pdf:
            text = ''
            tables = []
            for page in pdf.pages:
                text += page.extract_text()
                tables.extend(page.extract_tables())



        for table in tables:
            keyword = table[0][0]
            if 'PORTFÖY ÖZETİ' in keyword:
                pass
            elif 'YATIRIM İŞLEMLERİ' in keyword:
                self.read_asset_transactions(transaction_history, table)
            elif 'HESAP İŞLEMLERİ' in keyword:
                self.read_normal_transactions(transaction_history, table)
            elif 'TEMETTÜ İŞLEMLERİ' in keyword:
                if table[2] is not None:
                    self.read_dividend_transactions(transaction_history, table)
            elif 'HİSSE TRANSFERLERİ' in keyword:
                raise NotImplementedError
            

        return transaction_history

    def read_normal_transactions(self, transaction_history, normal_trasnactions):
        i = 0
        for row in normal_trasnactions: 
            if i>1:
                state = row[4]
                if state == 'Gerçekleşti':
                    date_string: str = row[1]
                    date_of_transaction :datetime = datetime.strptime(date_string, "%d/%m/%y %H:%M:%S")

                    genre: str = row[2]
                    amount, currency = row[5].split(' ')
                    amount = float(amount.replace(',','.'))
                    description:str = row[3]
                    if genre == 'Döviz Alış':
                        trans: Deposit = Deposit(date_of_transaction, amount, 'Midas', currency)
                    elif genre == 'Diğer Gelir':
                        if description == 'Nema Geliri':
                            trans: Income = Income(date_of_transaction, amount, 'Midas', currency)
                            trans.category = description
                    elif genre == 'Döviz Satış':
                        trans: Withdrawal = Withdrawal(date_of_transaction, amount, 'Midas', currency)
                    transaction_history.append(trans)
            i += 1

    def read_asset_transactions(self, transaction_history, asset_transactions):

        i = 0
        for row in asset_transactions:
            if i>1:
                state = row[4]
                if state == 'Gerçekleşti':
                    date_string = row[0]
                    ticker = row[2]
                    genre = row[3]
                    currency = row[5]
                    number = float(row[8].replace(',','.'))
                    price = float(row[9].replace(',','.'))
                    fee = float(row[10].replace(',','.'))
                    amount = float(row[11].replace(',','.'))

                    date_of_transaction :datetime = datetime.strptime(date_string, "%d/%m/%y %H:%M:%S")

                    if genre == 'Alış':
                        trans = BuyAsset(date_of_transaction,ticker, number, amount, 'Midas', currency, fee)
                    if genre == 'Satış':
                        trans = SellAsset(date_of_transaction,ticker, number, amount, 'Midas', currency, fee)
                    transaction_history.append(trans)

            i += 1

    def read_dividend_transactions(self, transaction_history, dividend_transactions):

        i = 0
        for row in dividend_transactions:
            if i > 1:
                date_string = row[0]
                ticker:str = row[1].split(' ')[0]
                gross, currency = row[2].split(' ')
                gross = float(gross.replace(',','.'))
                witholding = float(row[3].split(' ')[0].replace(',','.'))
                
                date_of_transaction :datetime = datetime.strptime(date_string, "%d/%m/%y")

                trans = Dividend(date_of_transaction, gross, self.account_name, currency = currency, fee = 0, ticker = ticker, witholding = witholding)

                transaction_history.append(trans)

            i += 1


class ReadUBS(ExtraitReader):
    """
    Reader for extrait data from UBS.
    """
    pass