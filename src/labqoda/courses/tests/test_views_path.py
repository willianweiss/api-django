import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPathView:
    @pytest.fixture
    def url(self):
        return reverse("path-list")

    def test_should_get_paths(self, url, paths_factory, authorized_client):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_get_paths_with_filter(
        self, url, paths_factory, authorized_client
    ):
        url = url + f"?name={paths_factory[0].name}"
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1

    def test_should_get_path_detail(self, path_factory, authorized_client):
        url = reverse("path-detail", args=[path_factory.slug])
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "name" in data
        assert "slug" in data
        assert "minidesc" in data
        assert "startDate" in data

    def test_should_path_return_not_found(self, authorized_client):

        url = reverse("path-detail", args=["fake-slug"])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
