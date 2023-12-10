from psedo_data_base import category_data, wallet_data
from datetime import datetime, timedelta
import sqlite3
import os
from logic_classes import *
import random

DATA_BASE_NAME = 'test.db'

DATA_HEADERS = {
    "TransactionType": {
        'category': 'text',
        'Type': 'text'},
    "Wallet": {
        'wallet_name': 'text',
        'initial_amount': 'real'},
    "TransactionHistory": {
        'transaction_id': 'integer',
        'transaction_date': 'text',
        'amount': 'real',
        'wallet_id_master': 'integer',
        'wallet_id_slave': 'integer',
        'type_id': 'integer',
        'description': 'text'}
}

if DATA_BASE_NAME in os.listdir():
    os.remove(DATA_BASE_NAME)

for key in DATA_HEADERS.keys():
    sql_text = 'CREATE TABLE ' + key + '('
    for sub_key, sub_value in DATA_HEADERS[key].items():
        sql_text += sub_key + ' ' + sub_value + ','
    sql_text = sql_text[:-1]
    sql_text += ')'


def create_db(data_base_name, data_headers_dict):
    conn = sqlite3.connect(data_base_name)
    c = conn.cursor()

    for key in data_headers_dict.keys():
        sql_text = 'CREATE TABLE ' + key + '('
        for sub_key, sub_value in data_headers_dict[key].items():
            sql_text += sub_key + ' ' + sub_value + ','
        sql_text = sql_text[:-1]
        sql_text += ')'

        c.execute(sql_text)

    conn.commit()
    conn.close()


def insert_transaction_type(transaction_type, data_base_name):
    conn = sqlite3.connect(data_base_name)
    conn.cursor()
    conn.execute(
        f"INSERT INTO TransactionType VALUES ('{transaction_type.category}', '{transaction_type.transaction_type}')")
    conn.commit()
    conn.close()


def insert_wallet_data(wallet, data_base_name):
    conn = sqlite3.connect(data_base_name)
    conn.cursor()
    conn.execute(f"INSERT INTO Wallet VALUES ('{wallet.wallet_name}', '{wallet.initial_amount}')")
    conn.commit()
    conn.close()


def insert_income_data(income, data_base_name):
    conn = sqlite3.connect(data_base_name)
    conn.cursor()
    conn.execute(
        f"INSERT INTO TransactionHistory VALUES ('{income.id}', '{income.transaction_date}','{income.amount}','{income.wallet_id_master}','{income.wallet_id_slave}','{income.transaction_type.transaction_type_id}','{income.description}')")
    conn.commit()
    conn.close()


def insert_expense_data(expense, data_base_name):
    conn = sqlite3.connect(data_base_name)
    conn.cursor()
    conn.execute(
        f"INSERT INTO TransactionHistory VALUES ('{expense.id}', '{expense.transaction_date}','{expense.amount}','{expense.wallet_id_master}','{expense.wallet_id_slave}','{expense.transaction_type.transaction_type_id}','{expense.description}')")
    conn.commit()
    conn.close()


def read_all(table_name, data_base_name):
    conn = sqlite3.connect(data_base_name)
    c = conn.cursor()
    c.execute(f"SELECT rowid,* FROM {table_name}")
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result


def random_date(start_date, end_date):
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date


def create_random_database():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    create_db(DATA_BASE_NAME, DATA_HEADERS)

    ## Transaction Type Construction
    transaction_type_counter = 0

    for category in category_data.keys():
        for transaction_type in category_data[category]:
            transaction_type_instance = TransactionType(transaction_type_counter, category.split('_')[-1],
                                                        transaction_type)

            insert_transaction_type(transaction_type_instance, DATA_BASE_NAME)
            transaction_type_counter += 1

    wallet_counter = 0
    wallet_list = []

    for item in wallet_data:
        wallet = Wallet(*item)

        wallet_counter += 1
        insert_wallet_data(wallet, DATA_BASE_NAME)
        wallet_list.append(wallet)

    wallet_data_list = read_all('Wallet', DATA_BASE_NAME)
    transaction_type_list = read_all('TransactionType', DATA_BASE_NAME)

    transaction_counter = 0
    for _ in range(1000):
        wallet = Wallet(*random.choice(wallet_data_list))
        tran_type = TransactionType(*random.choice(transaction_type_list))

        random_date_result = random_date(start_date, end_date)

        if tran_type.category == 'expense':
            trans = Expense(id=transaction_counter, transaction_date=random_date_result, amount=random.uniform(0, 2000),
                            wallet_id_master=wallet.wallet_id,
                            wallet_id_slave=0, description=tran_type.transaction_type, transaction_type=tran_type)
            insert_expense_data(trans, DATA_BASE_NAME)

        elif tran_type.category == 'income':
            trans = Income(id=transaction_counter, transaction_date=random_date_result, amount=random.uniform(0, 2000),
                           wallet_id_master=wallet.wallet_id,
                           wallet_id_slave=0, description=tran_type.transaction_type, transaction_type=tran_type)
            insert_income_data(trans, DATA_BASE_NAME)
        transaction_counter += 1


create_random_database()


def read_fast():
    for key in DATA_HEADERS.keys():
        result = read_all(key, DATA_BASE_NAME)
        print(result)
