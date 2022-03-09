import pytest
from model_bakery import baker


@pytest.fixture
def category_factory():
    return baker.make("catalog.Category")


@pytest.fixture
def categories_factory():
    return baker.make("catalog.Category", _quantity=10)


@pytest.fixture
def product_factory():
    return baker.make("catalog.Product")


@pytest.fixture
def products_factory():
    return baker.make("catalog.Product", _quantity=10)
