import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestModuleListViews:
    def test_should_get_certificate_course_example(
        self, certificate_course_factory, authorized_client
    ):
        url = reverse(
            "certificate-course-example", args=[certificate_course_factory.pk]
        )

        response = authorized_client.get(
            url, HTTP_ACCEPT="application/json; application/pdf"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"].lower() == "application/pdf"
        assert int(response["Content-Length"]) > 0

    def test_should_get_certificate_path_example(
        self, certificate_path_factory, authorized_client
    ):
        url = reverse(
            "certificate-path-example", args=[certificate_path_factory.pk]
        )

        response = authorized_client.get(
            url, HTTP_ACCEPT="application/json; application/pdf"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"].lower() == "application/pdf"
        assert int(response["Content-Length"]) > 0
