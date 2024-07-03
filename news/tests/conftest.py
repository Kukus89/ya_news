import pytest
from django.test.client import Client
from news.models import Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create_user(username='not_author')


@pytest.fixture
def author_client():
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client():
    client = Client()
    client.force_login(not_author)
    return client
