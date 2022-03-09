import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestThreadViews:
    @pytest.fixture
    def url(self):
        return reverse("thread-list")

    def test_should_get_threads(self, url, threads_factory, authorized_client):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_create_thread(
        self, url, content_factory, authorized_client
    ):
        title = "Thread Python"
        slug = "thread-python"
        payload = {
            "title": title,
            "slug": slug,
            "content_id": content_factory.pk,
        }

        response = authorized_client.post(url, data=payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["slug"] == slug

    def test_should_thread_return_bad_request_with_invalid_payloads(
        self, url, authorized_client,
    ):
        payload = {"name": "mame", "slug": "isso nao eh slug"}

        response = authorized_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_thread_detail(self, authorized_client, thread_factory):

        url = reverse("thread-detail", args=[thread_factory.slug])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["slug"] == thread_factory.slug

    def test_should_thread_return_not_found(self, authorized_client):

        url = reverse("thread-detail", args=["fake-slug"])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_update_thread(self, authorized_client, thread_factory):

        url = reverse("thread-detail", args=[thread_factory.slug])

        payload = {"title": "New name", "slug": "new-slug"}

        response = authorized_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["slug"] == payload["slug"]

    def test_should_thread_return_bad_request_in_partial_update(
        self, authorized_client, thread_factory
    ):
        url = reverse("thread-detail", args=[thread_factory.slug])

        payload = {"views": 50}

        response = authorized_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_return_not_found_in_update_thread(self, authorized_client):

        url = reverse("thread-detail", args=["fake-slug"])
        response = authorized_client.put(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_partial_update_thread(
        self, authorized_client, thread_factory
    ):

        url = reverse("thread-detail", args=[thread_factory.slug])

        payload = {"views": 50}

        response = authorized_client.patch(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["views"] == payload["views"]

    def test_should_not_found_in_partial_update_thread(
        self, authorized_client
    ):

        url = reverse("thread-detail", args=["fakej-slug"])
        response = authorized_client.patch(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_delete_thread(self, authorized_client, thread_factory):

        url = reverse("thread-detail", args=[thread_factory.slug])
        response = authorized_client.delete(url, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_not_found_in_delete_thread(self, authorized_client):

        url = reverse("thread-detail", args=["fake-slug"])
        response = authorized_client.delete(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
