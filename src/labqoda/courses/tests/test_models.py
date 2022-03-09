import pytest


@pytest.mark.django_db
class TestCourseModels:
    def test_should_get_subject_title(self, subject_factory):
        assert str(subject_factory) == f"{subject_factory.title}"

    def test_should_get_course_name(self, course_factory):
        assert str(course_factory) == f"{course_factory.name}"

    def test_should_get_course_absolute_url(self, course_factory):
        assert course_factory.get_absolute_url()

    def test_should_get_content_str(self, content_factory):
        assert "Content" in str(content_factory)

    def test_should_get_content_item(self, item_code_factory):
        assert str(item_code_factory) == "self.order"
