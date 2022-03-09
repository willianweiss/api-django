import pytest


@pytest.mark.django_db
class TestCategoryModels:
    def test_should_get_category_name(self, category_factory):
        assert str(category_factory) == f"{category_factory.name}"


@pytest.mark.django_db
class TestProductModels:
    def test_should_get_category_name(self, product_factory):
        assert str(product_factory) == f"{product_factory.name}"
