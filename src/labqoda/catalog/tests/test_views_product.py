import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductViews:
    @pytest.fixture
    def url(self):
        return reverse("product-list")

    def test_should_get_product(
        self, url, products_factory, authorized_client
    ):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_get_product_with_filter(
        self, url, products_factory, authorized_client
    ):
        url = url + f"?category__slug={products_factory[0].category.slug}"
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1

    def test_should_get_product_detail(
        self, authorized_client, product_factory
    ):

        url = reverse("product-detail", args=[product_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == product_factory.pk

    def test_should_return_not_found(self, authorized_client):

        url = reverse("product-detail", args=[232389])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
