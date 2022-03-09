from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

target_namespace = "labqoda.helpers.email.base"


@pytest.mark.django_db
class TestContactViews:
    @pytest.fixture
    def url(self):
        return reverse("contact-list")

    @pytest.fixture
    def mock_send_mail(self):
        with mock.patch(f"{target_namespace}.send_mail_contact") as mock_token:
            yield mock_token

    def test_should_get_contacts(
        self, url, contacts_factory, authorized_client
    ):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_create_contact(
        self, url, contact_payload, authorized_client
    ):
        response = authorized_client.post(
            url, data=contact_payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == contact_payload["email"]

    def test_should_create_contact_with_mock_send_mail(
        self,
        url,
        contact_payload,
        authorized_client,
        mock_send_mail,
        default_contact_email,
    ):
        mock_send_mail.return_value = True

        response = authorized_client.post(
            url, data=contact_payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == contact_payload["email"]

    def test_should_contact_return_bad_request_with_invalid_payloads(
        self, url, authorized_client,
    ):
        payload = {"name": "mame"}

        response = authorized_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_contact_detail(
        self, authorized_client, contact_factory
    ):

        url = reverse("contact-detail", args=[contact_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == contact_factory.pk

    def test_should_return_not_found(self, authorized_client):

        url = reverse("contact-detail", args=[232389])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
