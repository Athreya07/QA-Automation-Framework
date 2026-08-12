"""
data_generator.py
==========================================================
Faker-based random test data generator. Used mainly for
checkout information (first name, last name, postal code)
so tests aren't hardcoded and can be run repeatedly with
fresh data.
==========================================================
"""

from faker import Faker

fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_checkout_info() -> dict:
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "postal_code": fake.postcode(),
        }

    @staticmethod
    def generate_first_name() -> str:
        return fake.first_name()

    @staticmethod
    def generate_last_name() -> str:
        return fake.last_name()

    @staticmethod
    def generate_postal_code() -> str:
        return fake.postcode()
