import pytest
from model_bakery import baker


@pytest.fixture
def contact_factory():
    return baker.make("configurations.Contact")


@pytest.fixture
def contacts_factory():
    return baker.make("configurations.Contact", _quantity=10)


@pytest.fixture
def default_contact_email():
    return baker.make("configurations.DefaultContactEmail")


@pytest.fixture
def default_instructor():
    return baker.make("configurations.DefaultInstructor")


@pytest.fixture
def contact_payload():
    return {
        "name": "Silvio Santos",
        "email": "silvio@sbt.br",
        "message": "Tem curso de assitente de palco?",
    }
