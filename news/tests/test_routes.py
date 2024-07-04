import pytest
from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (
        ("news:detail", pytest.lazy_fixture("news_id")),
        ("news:home", None),
        ("users:login", None),
        ("users:logout", None),
        ("users:signup", None),
    )
)
def test_pages_available_for_anonim_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    "name",
    (
        ("news:edit", "news:delete")
    )
)
def test_comment_pages_available_for_author(
    parametrized_client,
    expected_status,
    name,
    comment
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture("news_id")),
        ('news:delete', pytest.lazy_fixture("news_id")),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=(args))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
