import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCoursesListViews:
    @pytest.fixture
    def url(self):
        return reverse("courses-list")

    def test_should_get_courses(self, url, courses_factory, authorized_client):
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 1

    def test_should_get_courses_with_name_filter(
        self, url, courses_factory, authorized_client
    ):
        url = url + f"?name={courses_factory[0].name}"
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1

    def test_should_create_course(
        self, url, course_payload, authorized_client, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        response = authorized_client.post(
            url, data=course_payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_course_return_bad_request_with_invalid_payloads(
        self, url, course_payload, authorized_client, get_authorized_user
    ):
        payload = {"username": "mame", "password": "1234"}

        response = authorized_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_get_course_detail(self, authorized_client, course_factory):

        url = reverse("courses-detail", args=[course_factory.slug])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == course_factory.pk

    def test_should_course_return_not_found(self, authorized_client):

        url = reverse("courses-detail", args=["fake-slug"])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_update_course_with_patch(
        self, authorized_client, course_factory, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("courses-update-delete", args=[course_factory.pk])

        new_name = "Xtop"
        payload = {
            "name": new_name,
        }

        response = authorized_client.patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == new_name

    def test_should_course_return_not_found_with_update(
        self, authorized_client, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("courses-update-delete", args=[23232])
        payload = {
            "name": "xxx",
        }

        response = authorized_client.patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_permission_error_update_course(
        self, authorized_client, course_factory
    ):
        url = reverse("courses-update-delete", args=[course_factory.pk])
        payload = {"name": "xptp"}

        response = authorized_client.patch(url, data=payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_should_delete_course(
        self, authorized_client, course_factory, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("courses-update-delete", args=[course_factory.pk])

        response = authorized_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_course_return_not_found_with_delete(
        self, authorized_client, get_authorized_user
    ):
        get_authorized_user.is_staff = True
        get_authorized_user.save()

        get_authorized_user.refresh_from_db()

        url = reverse("courses-update-delete", args=[23232])

        response = authorized_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_permission_error_delete_course(
        self, authorized_client, course_factory
    ):
        url = reverse("courses-update-delete", args=[course_factory.pk])
        payload = {"name": "xptp"}

        response = authorized_client.delete(url, data=payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
