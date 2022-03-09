import pytest


@pytest.mark.django_db
class TestThreadModels:
    def test_should_get_thread_title(self, thread_factory):
        assert str(thread_factory) == f"{thread_factory.title}"

    def test_should_get_absolute_url(self, thread_factory):
        assert bool(thread_factory.slug in thread_factory.get_absolute_url())


@pytest.mark.django_db
class TestReplayModels:
    def test_should_get_replay_initial_text(self, reply_factory):
        assert str(reply_factory) == f"{reply_factory.reply[:100]}"
