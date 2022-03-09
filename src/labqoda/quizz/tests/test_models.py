import pytest


@pytest.mark.django_db
class TestCategoryModels:
    def test_should_get_quizz_title(self, quizz_factory):
        assert str(quizz_factory) == f"{quizz_factory.title}"

    def test_should_get_quizz_choice_text(self, quizz_choice_factory):
        assert str(quizz_choice_factory) == f"{quizz_choice_factory.text}"

    def test_should_get_quizz_question_text(self, quizz_question_factory):
        assert str(quizz_question_factory) == f"{quizz_question_factory.text}"
