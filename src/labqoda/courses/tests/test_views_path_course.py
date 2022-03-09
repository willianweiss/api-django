import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPathCourseView:
    def test_should_get_paths_courses(
        self, paths_courses_factory, authorized_client
    ):
        url = reverse(
            "path-course-list", args=[paths_courses_factory[0].path.slug]
        )
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(data) >= 1

    def test_should_path_course_return_not_found(self, authorized_client):

        url = reverse("path-course-list", args=["fake-slug"])
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_get_path_course_detail(
        self, path_course_factory, authorized_client
    ):
        url = reverse(
            "path-course-detail",
            args=[path_course_factory.path.slug, path_course_factory.pk],
        )
        response = authorized_client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "order" in data

    def test_should_path_course_pk_return_not_found(
        self, path_course_factory, authorized_client
    ):
        url = reverse(
            "path-course-detail",
            args=[path_course_factory.path.slug, 84938934],
        )
        response = authorized_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
