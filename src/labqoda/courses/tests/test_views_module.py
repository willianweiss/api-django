import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestModuleListViews:
    def test_should_get_modules(self, modules_factory, authorized_client):
        url = reverse("module-list", args=[modules_factory[0].course.slug])
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) >= 1

    def test_should_module_return_not_found_with_list(self, authorized_client):

        url = reverse("module-list", args=["fake-slug"])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_create_module(
        self,
        authorized_client,
        module_payload,
        course_factory,
        get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("module-list", args=[course_factory.slug])
        response = authorized_client.post(
            url, data=module_payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_module_return_bad_request_with_invalid_payloads(
        self,
        authorized_client,
        module_payload,
        course_factory,
        get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        module_payload.pop("title")

        url = reverse("module-list", args=[course_factory.slug])
        response = authorized_client.post(
            url, data=module_payload, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_module_return_not_found_with_invalid_course(
        self, authorized_client, module_payload, get_authorized_user,
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("module-list", args=[98493])
        response = authorized_client.post(
            url, data=module_payload, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_get_module_detail(self, authorized_client, module_factory):

        url = reverse(
            "module-detail",
            args=[module_factory.course.slug, module_factory.pk],
        )
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == module_factory.pk

    def test_should_course_return_not_found(
        self, module_factory, authorized_client
    ):

        url = reverse("module-detail", args=["fake-slug", module_factory.pk])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_module_return_not_found_with_detail(
        self, module_factory, authorized_client
    ):

        url = reverse(
            "module-detail", args=[module_factory.course.slug, 849348]
        )
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
