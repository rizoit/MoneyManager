import pytest
from logic_classes import *


def test_income_category_equality():
    inc_cat_1 = IncomeCategory(1, "cat1")
    inc_cat_2 = IncomeCategory(1, "cat1")

    assert inc_cat_1 == inc_cat_2


def test_expense_category_equality():
    exp_cat_1 = ExpenseCategory(1, "cat1")
    exp_cat_2 = ExpenseCategory(1, "cat1")

    assert exp_cat_1 == exp_cat_2
