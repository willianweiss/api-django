import pytest


@pytest.mark.django_db
class TestDefaultInstructorModels:
    def test_should_get_instructor_name(self, default_instructor):
        assert (
            str(default_instructor) == f"{default_instructor.instructor.email}"
        )


@pytest.mark.django_db
class TestDefaultContactEmailModels:
    def test_should_get_default_contact_email(self, default_contact_email):
        assert str(default_contact_email) == f"{default_contact_email.email}"


@pytest.mark.django_db
class TestContactModels:
    def test_should_get_contact_name(self, contact_factory):
        assert str(contact_factory) == f"nome: {contact_factory.name}"
