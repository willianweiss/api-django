from collections import namedtuple
from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from model_bakery import baker
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
)
from rest_framework.test import APIClient

OAuth2Token = namedtuple(
    "oauth2token", ["dev_user", "application", "access_token"]
)

Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


@pytest.fixture
def client():
    client = APIClient()

    return client


def generate_user():
    user_model = get_user_model()
    dev_user = user_model.objects.create_user("dev@dev.dev", "123mudar")
    return dev_user


def generate_application(user=None):
    application_model = get_application_model()
    application = application_model.objects.first()

    if application:
        return application

    if user is None:
        user = generate_user()

    application = application_model.objects.create(
        name="Test Application",
        user=user,
        client_type=application_model.CLIENT_CONFIDENTIAL,
        authorization_grant_type=application_model.GRANT_CLIENT_CREDENTIALS,
    )

    return application


def generate_oauth2_token(application=None):
    if application is None:
        application = generate_application()

    access_token = AccessToken.objects.create(
        user=application.user,
        scope=" ".join(settings.OAUTH2_PROVIDER["SCOPES"].keys()),
        expires=timezone.now() + timedelta(seconds=3600),
        token="screct-access-token-key",
        application=application,
    )

    return OAuth2Token(
        dev_user=application.user,
        application=application,
        access_token=access_token,
    )


@pytest.fixture
def application():
    return generate_application()


@pytest.fixture
def authorized_client(client, application):
    oauth2token = generate_oauth2_token(application)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {oauth2token.access_token.token}"
    )

    return client


@pytest.fixture
def get_authorized_user():
    return UserModel.objects.filter(email="dev@dev.dev").first()


@pytest.fixture
def user_factory():
    return baker.make("users.User")
