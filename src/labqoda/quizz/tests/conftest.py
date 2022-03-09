import pytest
from model_bakery import baker


@pytest.fixture
def quizz_factory():
    return baker.make("quizz.Quizz")


@pytest.fixture
def quizzes_factory():
    return baker.make("quizz.Quizz", _quantity=10)


@pytest.fixture
def quizz_choice_factory():
    return baker.make("quizz.Choice", question__justification="<h1>test</h1>")


@pytest.fixture
def quizz_question_factory():
    return baker.make("quizz.Question", justification="<h1>test</h1>")
