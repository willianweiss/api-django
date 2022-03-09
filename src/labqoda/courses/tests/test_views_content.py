import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestModuleListViews:
    def test_should_get_contents(self, contents_factory, authorized_client):
        url = reverse("content-list", args=[contents_factory[0].module.pk])
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) >= 1

    def test_should_module_return_not_found_with_list(self, authorized_client):

        url = reverse("content-list", args=[455435])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_create_content(
        self,
        authorized_client,
        module_factory,
        content_payload,
        get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        content_payload["instructor"] = get_authorized_user.pk

        url = reverse("content-list", args=[module_factory.pk])
        response = authorized_client.post(
            url, data=content_payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_content_return_bad_request_with_invalid_payloads(
        self,
        authorized_client,
        module_factory,
        content_payload,
        get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("content-list", args=[module_factory.pk])
        response = authorized_client.post(
            url, data=content_payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_content_return_not_found_with_invalid_module(
        self, authorized_client, module_payload, get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("content-list", args=[98493])
        response = authorized_client.post(
            url, data=module_payload, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_get_content_detail(
        self, authorized_client, content_factory
    ):

        url = reverse(
            "content-detail",
            args=[content_factory.module.pk, content_factory.pk],
        )
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == content_factory.pk

    def test_should_return_not_found_with_invalid_module(
        self, content_factory, authorized_client
    ):

        url = reverse("content-detail", args=[34343, content_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_content_return_not_found_with_detail(
        self, module_factory, authorized_client
    ):
        url = reverse("module-detail", args=[module_factory.pk, 849348])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_update_content_with_patch(
        self,
        authorized_client,
        content_factory,
        get_authorized_user,
        content_payload,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse(
            "content-detail",
            args=[content_factory.module.pk, content_factory.pk],
        )

        payload = {
            "duration": "20 minutos",
        }

        response = authorized_client.patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["duration"] == payload["duration"]

    def test_should_content_return_not_found_with_update(
        self, authorized_client, get_authorized_user, content_factory
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("content-detail", args=[323232, content_factory.pk],)
        payload = {
            "duration": "20 minutos",
        }

        response = authorized_client.patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_delete_content(
        self, authorized_client, content_factory, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse(
            "content-detail",
            args=[content_factory.module.pk, content_factory.pk],
        )

        response = authorized_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_content_return_not_found_with_delete(
        self, authorized_client, get_authorized_user, content_factory
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse(
            "content-detail", args=[content_factory.module.pk, 43434],
        )

        response = authorized_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_get_content_items_detail(
        self, authorized_client, content_factory
    ):
        url = reverse(
            "content-items",
            args=[content_factory.module.pk, content_factory.pk],
        )
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "videos" in data
        assert "images" in data
        assert "texts" in data
        assert "files" in data
        assert "quizz" in data
