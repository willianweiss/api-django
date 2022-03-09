import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestQuizzViews:
    @pytest.fixture
    def url(self):
        return reverse("quizz-list")

    def test_should_get_quizz(self, url, quizzes_factory, authorized_client):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_get_quizz_detail(self, authorized_client, quizz_factory):

        url = reverse("quizz-detail", args=[quizz_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == quizz_factory.pk

    def test_should_quizz_return_not_found(self, authorized_client):

        url = reverse("quizz-detail", args=[232389])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
