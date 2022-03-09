import pytest
from model_bakery import baker


@pytest.fixture
def certificate_course_factory():
    return baker.make(
        "certificates.CourseCertificate", text="<h1>Certificate</h1>"
    )


@pytest.fixture
def certificate_path_factory():
    return baker.make(
        "certificates.PathCertificate", text="<h1>Certificate</h1>"
    )


@pytest.fixture
def certificate_user_factory():
    return baker.make(
        "certificates.UserCertificate", text="<h1>Certificate</h1>"
    )
