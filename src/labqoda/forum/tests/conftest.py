import pytest
from model_bakery import baker


@pytest.fixture
def thread_factory():
    return baker.make("forum.Thread")


@pytest.fixture
def threads_factory():
    return baker.make("forum.Thread", _quantity=10)


@pytest.fixture
def reply_factory():
    return baker.make("forum.Reply")


@pytest.fixture
def replys_factory():
    return baker.make("forum.Reply", _quantity=10)


@pytest.fixture
def content_factory():
    return baker.make("courses.Content")
