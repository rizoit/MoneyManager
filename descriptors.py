from datetime import datetime

import psedo_data_base
from psedo_data_base import *


class FloatValidator:
    """
   A descriptor that checks the type of the attributes. If the attribute could be converted into a float,
   it converts it in the set method, and if not, it raises a ValueError. It also checks the attribute value
   and if it is negative, it raises a ValueError.
   """

    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        """
       Getter method for the descriptor.
       """
        return self.value

    def __set__(self, instance, value):
        """
       Setter method for the descriptor. It checks if the value can be converted into a float. If it can,
       it converts it. If it can't, it raises a ValueError. It also checks if the value is negative and
       if it is, it raises a ValueError.
       """
        try:
            float_value = float(value)
            if float_value < 0:
                raise ValueError("Value cannot be negative")
            self.value = float_value
        except TypeError:
            raise TypeError(f"{self.value} must be float")


class IntValidator:
    """
   A descriptor that checks the type of the attributes. If the attribute could be converted into a float,
   it converts it in the set method, and if not, it raises a ValueError. It also checks the attribute value
   and if it is negative, it raises a ValueError.
   """

    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        """
       Getter method for the descriptor.
       """
        return self.value

    def __set__(self, instance, value):
        """
       Setter method for the descriptor. It checks if the value can be converted into a float. If it can,
       it converts it. If it can't, it raises a ValueError. It also checks if the value is negative and
       if it is, it raises a ValueError.
       """

        try:
            int_value = int(value)
            if int_value < 0:
                raise ValueError("Value cannot be negative")
            self.value = int_value
        except ValueError:
            raise ValueError(f"{self.value} must be integer")


class StringValidator:
    """
   A descriptor that checks if an attribute is a string and sets a maximum length limit.
   """

    def __init__(self, max_length):
        """
       Initialize the descriptor with a maximum length.

       :param max_length: The maximum length of the string.
       """
        self.max_length = max_length

    def __get__(self, instance, owner):
        """
       Get the value of the attribute.

       :param instance: The instance that the attribute belongs to.
       :param owner: The owner of the attribute.
       :return: The value of the attribute.
       """
        return self.value

    def __set__(self, instance, value):
        """
       Set the value of the attribute.

       :param instance: The instance that the attribute belongs to.
       :param value: The value to set the attribute to.
       """
        if value is None:
            value = ''
        if not isinstance(value, str):
            raise TypeError("Value must be a string.")
        elif len(value) > self.max_length:
            raise ValueError(f"String length must be less than or equal to {self.max_length}.")

        self.value = value


class DateTimeValidator:
    """
   A descriptor that checks if an attribute is a datetime object. If not, it checks if it's a string in the format "DD/MM/YYYY HH:MM".
   If it is, it converts it to a datetime object and assigns it to the attribute. If it's not, it raises a TypeError.
   """

    def __get__(self, instance, owner):
        """
       Get the value of the attribute.
       """
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        """
       Set the value of the attribute. If the value is not a datetime object, it checks if it's a string in the format "DD/MM/YYYY HH:MM".
       If it is, it converts it to a datetime object and assigns it to the attribute. If it's not, it raises a TypeError.
       """
        if isinstance(value, datetime):
            instance.__dict__[self.name] = value
        elif isinstance(value, str):
            try:
                instance.__dict__[self.name] = datetime.strptime(value, "%d-%m-%Y %H:%M")
            except ValueError:
                raise TypeError("Invalid datetime format. Expected format is 'DD/MM/YYYY HH:MM'")
        else:
            raise TypeError("Invalid type. Expected datetime object or string in the format 'DD/MM/YYYY HH:MM'")

    def __set_name__(self, owner, name):
        """
       Set the name of the attribute.
       """
        self.name = name


class CategoryValidator:
    """
   A descriptor that checks the type of category.It recognizes type of transaction and If category and transaction are not compatible, raises type error.
   """

    def __set_name__(self, owner_class, property_name):

        self.property_name = property_name
        self.owner_class = owner_class

    def __get__(self, instance, owner):
        """
       Get the value of the attribute.
       """

        return instance.__dict__[self.property_name]

    def __set__(self, instance, value):
        from logic_classes import TransactionType

        if not isinstance(value, TransactionType):
            raise TypeError(f"{value} must be TransactionType")

        set_name = self.property_name + '_' + self.owner_class.__name__.lower()


        if getattr(value, self.property_name) in psedo_data_base.category_data[set_name]:
            instance.__dict__[self.property_name] = value
        else:
            raise TypeError(f"{value} is not a valid {self.owner_class.__name__} category")
