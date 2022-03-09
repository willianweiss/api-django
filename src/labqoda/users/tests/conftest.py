import pytest

from labqoda.courses.tests.baker_recipes import (
    course,
    course_enrollment,
    course_progress,
    enrollment,
    path_enrollment,
)


@pytest.fixture
def user_payload():
    return {
        "username": "doido",
        "first_name": "Doido",
        "last_name": "Varido",
        "fullname": "Doido Varido",
        "email": "doido@doido.com",
        "is_staff": False,
        "is_active": True,
        "is_trusty": True,
    }


@pytest.fixture
def dashboard_data(get_authorized_user):
    _enrollment = enrollment.make(user=get_authorized_user)
    _path_enrollment = path_enrollment.make(enrollment=_enrollment)
    _course_enrollment = course_enrollment.make(enrollment=_enrollment)
    _course = course.make()
    course_progress.make(
        user=get_authorized_user,
        course_enrollment=_course_enrollment,
        path_enrollment=_path_enrollment,
        course=_course,
    )
    yield
