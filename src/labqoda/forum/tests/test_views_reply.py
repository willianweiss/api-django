import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestreplyViews:
    @pytest.fixture
    def url(self):
        return reverse("reply-list")

    def test_should_get_replys(self, url, replys_factory, authorized_client):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_create_reply(
        self, url, thread_factory, authorized_client, user_factory
    ):

        payload = {
            "reply": "Xpto bla bla",
            "correct": True,
            "status": "APPROVED",
            "thread_id": thread_factory.pk,
            "author_id": user_factory.pk,
        }

        response = authorized_client.post(url, data=payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_should_create_reply_comment(
        self, url, reply_factory, authorized_client, user_factory
    ):

        payload = {
            "reply": "Xpto bla bla",
            "comment_id": reply_factory.pk,
            "correct": True,
            "status": "APPROVED",
            "thread_id": reply_factory.thread.pk,
            "author_id": user_factory.pk,
        }

        response = authorized_client.post(url, data=payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_should_reply_return_bad_request_with_invalid_payloads(
        self, url, authorized_client,
    ):
        payload = {"reply": "mame", "slug": " nao tem slug"}

        response = authorized_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_reply_detail(self, authorized_client, reply_factory):

        url = reverse("reply-detail", args=[reply_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["reply"] == reply_factory.reply

    def test_should_reply_return_not_found(self, authorized_client):

        url = reverse("reply-detail", args=[4343])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_update_reply(self, authorized_client, reply_factory):

        url = reverse("reply-detail", args=[reply_factory.pk])

        payload = {
            "reply": "Xpto bla bla",
            "correct": True,
            "status": "APPROVED",
        }

        response = authorized_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["reply"] == payload["reply"]

    def test_should_reply_return_bad_request_in_partial_update(
        self, authorized_client, reply_factory
    ):
        url = reverse("reply-detail", args=[reply_factory.pk])

        payload = {"status": "ok"}

        response = authorized_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_return_not_found_in_update_reply(self, authorized_client):

        url = reverse("reply-detail", args=[9485])
        response = authorized_client.put(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_partial_update_reply(
        self, authorized_client, reply_factory
    ):

        url = reverse("reply-detail", args=[reply_factory.pk])

        payload = {"reply": "new text in reply"}

        response = authorized_client.patch(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["reply"] == payload["reply"]

    def test_should_not_found_in_partial_update_reply(self, authorized_client):

        url = reverse("reply-detail", args=[5948549])
        response = authorized_client.patch(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_delete_reply(self, authorized_client, reply_factory):

        url = reverse("reply-detail", args=[reply_factory.pk])
        response = authorized_client.delete(url, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_not_found_in_delete_reply(self, authorized_client):

        url = reverse("reply-detail", args=[8945849])
        response = authorized_client.delete(url, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
