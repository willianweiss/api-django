import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserViews:
    @pytest.fixture
    def url_register(self):
        return reverse("user-register")

    @pytest.fixture
    def url_detail(self):
        return reverse("user-detail")

    def test_should_create_user(self, url_register, client):
        payload = {
            "email": "dev@test.com",
            "password": "29084D34ku93#$",
        }

        response = client.post(url_register, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_user_return_bad_request_with_invalid_payloads(
        self, url_register, client,
    ):
        payload = {"username": "mame", "password": "1234"}

        response = client.post(url_register, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_user_return_bad_request_with_invalid_password(
        self, url_register, client,
    ):
        payload = {"email": "dev@test.com", "password": "1234"}

        response = client.post(url_register, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_user_detail(self, url_detail, authorized_client):
        response = authorized_client.get(url_detail)

        assert response.status_code == status.HTTP_200_OK

    def test_should_user_return_not_autorized(self, url_detail, client):
        response = client.get(url_detail)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_update_user(
        self, url_detail, authorized_client, user_payload
    ):
        response = authorized_client.put(
            url_detail, data=user_payload, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user_payload["username"]

    def test_should_user_return_bad_request_in_partial_update(
        self, url_detail, authorized_client, user_factory
    ):
        payload = {"username": "my-new-username"}

        response = authorized_client.put(
            url_detail, data=payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_return_not_authorized_in_update_user(
        self, url_detail, client
    ):
        response = client.put(url_detail, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_partial_update_user(
        self, url_detail, authorized_client, user_factory
    ):
        payload = {"username": "diodoido"}

        response = authorized_client.patch(
            url_detail, data=payload, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == payload["username"]

    def test_should_not_authorized_in_partial_update_user(
        self, url_detail, client
    ):
        response = client.patch(url_detail, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_delete_user(
        self, url_detail, authorized_client, user_factory
    ):
        response = authorized_client.delete(url_detail, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_not_authorized_in_delete_user(self, url_detail, client):

        response = client.delete(url_detail, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_user_change_password(
        self, authorized_client,
    ):
        url = reverse("password-change")

        payload = {"oldPassword": "123mudar", "newPassword": "mudar2020@2020"}

        response = authorized_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_should_not_authorized_in_user_change_password(self, client):
        url = reverse("password-change")

        payload = {"oldPassword": "123mudar", "newPassword": "mudar2020@2020"}

        response = client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_get_user_dashboard(
        self, url_detail, authorized_client, dashboard_data
    ):

        url = reverse("user-dashboard")
        response = authorized_client.get(url)
        assert response.status_code == status.HTTP_200_OK
