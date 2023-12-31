import pytest
from logic_classes import *

trans_general_purpose = Transaction(id=1, amount=100.0, transaction_date="12-11-2018 09:15", wallet_id_master=1,
                                    description="description")


class TestIntValidator:

    def test_int_validator_0(self):
        assert trans_general_purpose.id == 1
        assert trans_general_purpose.wallet_id_master == 1

    def test_int_validator_1(self):
        assert type(trans_general_purpose.id) == int

    def test_int_validator_2(self):
        assert type(trans_general_purpose.wallet_id_master) == int

    def test_int_validator_3(self):
        with pytest.raises(ValueError) as exc_info:
            Transaction(id="one", amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                        description="description")
            print(exc_info)

    def test_int_validator_4(self):
        with pytest.raises(ValueError) as exc_info:
            Transaction(id=-3, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                        description="description")
            print(exc_info)

    def test_int_validator_shared_instance(self):
        trans_1 = Transaction(id=1, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description")
        trans_2 = Transaction(id=2, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description")

        assert trans_1.id != trans_2.id


class TestFloatValidator:

    def test_float_validator_0(self):
        assert trans_general_purpose.amount == 100.0

    def test_int_validator_1(self):
        assert type(trans_general_purpose.amount) == float

    def test_int_validator_3(self):
        with pytest.raises(ValueError) as exc_info:
            Transaction(id=4, amount=-100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                        description="description")
            print(exc_info)

    def test_float_validator_shared_instance(self):
        trans_1 = Transaction(id=1, amount=100.0, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description")
        trans_2 = Transaction(id=2, amount=200.1, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description")

        assert trans_1.amount != trans_2.amount


class TestStringValidator:

    def test_string_validator_0(self):
        assert trans_general_purpose.description == "description"

    def test_string_validator_1(self):
        assert type(trans_general_purpose.description) == str

    def test_string_validator_3(self):
        with pytest.raises(ValueError) as exc_info:
            Transaction(id=4, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                        description="a" * 201)
            print(exc_info)

    def test_string_validator_4(self):
        with pytest.raises(TypeError) as exc_info:
            Transaction(id=4, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                        description=12)
            print(exc_info)

    def test_string_validator_shared_instance(self):
        trans_1 = Transaction(id=1, amount=100.0, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description_1")
        trans_2 = Transaction(id=2, amount=200.1, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description_2")

        assert trans_1.description != trans_2.description

    def test_empty_descriptor(self):
        trans = Transaction(1, "12-11-2018 09:15", 100, 1)
        assert trans.description == ''


class TestDatetimeValidator:

    def test_datetime_validator_0(self):
        assert trans_general_purpose.transaction_date == datetime.strptime("12-11-2018 09:15", "%d-%m-%Y %H:%M")

    def test_datetime_validator_1(self):
        trans = Transaction(id=4, amount=100, transaction_date=datetime.now(), wallet_id_master=1,
                            description="description")
        assert trans.transaction_date == datetime.now()

    def test_datetime_validator_2(self):
        with pytest.raises(ValueError) as exc_info:
            Transaction(id=4, amount=100, transaction_date="12-11-2018 09:15", wallet_id_master=1,
                        description="a" * 201)
            print(exc_info)

    def test_datetime_validator_shared_instance(self):
        trans_1 = Transaction(id=1, amount=100.0, transaction_date="12-11-2018 09:15", wallet_id_master=1.2,
                              description="description_1")
        trans_2 = Transaction(id=2, amount=200.1, transaction_date="12-11-2018 10:15", wallet_id_master=1.2,
                              description="description_2")

        assert trans_1.transaction_date != trans_2.transaction_date



class TestCategoryValidator:
    def test_is_category_string_for_income(self):
        with pytest.raises(TypeError) as exc_info:
            Income(1, datetime.now(), 100, 1, "", 16)
            print(exc_info)

    def test_is_category_string_for_expense(self):
        with pytest.raises(TypeError) as exc_info:
            Expense(1, datetime.now(), 100, 1, "", 16)
            print(exc_info)

    def test_is_transaction_income_exist_income_neg(self):
        trans = TransactionType(1, "Income", "MoneyLoundary")

        with pytest.raises(TypeError) as exc_info:
            Income(1, datetime.now(), 100, 1, "", trans)
            print(exc_info)

    def test_is_transaction_income_exist_pos(self):
        trans = TransactionType(1, "Income", "Salary")
        Income(1, datetime.now(), 100, 1, 1, 'asd', trans)

    def test_is_transaction_expense_exist_neg(self):
        with pytest.raises(TypeError) as exc_info:
            trans = TransactionType(1, "Expense", "Criminal Act")
            Expense(1, datetime.now(), 100, 1, "", trans)
            print(exc_info)

    def test_is_transaction_expense_exist_pos(self):
        trans = TransactionType(1, "Expense", "Rent")
        Expense(1, datetime.now(), 100, 1, 0, "", trans)

    def test_category_validator_shared_instance(self):
        trans_1 = TransactionType(1, "Expense", "Rent")
        trans_2 = TransactionType(1, "Expense", "Pet")

        assert trans_1.transaction_type != trans_2.transaction_type
