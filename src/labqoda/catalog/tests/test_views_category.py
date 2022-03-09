import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCategoryViews:
    @pytest.fixture
    def url(self):
        return reverse("category-list")

    def test_should_get_category(
        self, url, categories_factory, authorized_client
    ):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_get_category_detail(
        self, authorized_client, category_factory
    ):

        url = reverse("category-detail", args=[category_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == category_factory.pk

    def test_should_category_return_not_found(self, authorized_client):

        url = reverse("category-detail", args=[232389])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
