import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCoursesEnrollmentViews:
    def test_should_create_course_enrollment(
        self, course_factory, authorized_client
    ):
        url = reverse("courses-enrollment", args=[course_factory.slug])

        response = authorized_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert "code" in response.json()

    def test_should_return_ok_if_exists_course_enrollment(
        self, course_factory, authorized_client
    ):
        url = reverse("courses-enrollment", args=[course_factory.slug])

        response = authorized_client.post(url)
        assert response.status_code == status.HTTP_200_OK

        response = authorized_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert "code" in response.json()

    def test_should_return_not_found_with_course_enrollment(
        self, authorized_client
    ):
        url = reverse("courses-enrollment", args=["fake-slug"])

        response = authorized_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
