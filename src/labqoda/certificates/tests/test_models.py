import pytest


@pytest.mark.django_db
class TestCertificatesModels:
    def test_should_get_course_certificate(self, certificate_course_factory):
        assert (
            str(certificate_course_factory)
            == f"{certificate_course_factory.title}"
        )

    def test_should_get_path_certificate(self, certificate_path_factory):
        assert (
            str(certificate_path_factory)
            == f"{certificate_path_factory.title}"
        )

    def test_should_get_user_certificate(self, certificate_user_factory):
        assert (
            str(certificate_user_factory)
            == f"{certificate_user_factory.certificate_code}"
        )
