from enum import Enum

from labqoda.helpers.database.enum import EnumDatabaseMixin


class MyFakeEnum(EnumDatabaseMixin, Enum):
    APPLE = "apple"
    PEAR = "pear"
    BANANA = "banana"


class TestEnumDatabaseMixin:
    def test_should_return_number_of_max_enum_length(self):
        assert MyFakeEnum.get_database_max_length() == 6

    def test_should_return_database_choices(self):
        expected = [("apple", "apple"), ("pear", "pear"), ("banana", "banana")]

        assert MyFakeEnum.get_database_choices() == expected
