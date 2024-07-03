import pytest
from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "name",
    ("news:home", "users:login", "users:logout", "users:signup")
)
def test_homepage_available_for_not_registered_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK