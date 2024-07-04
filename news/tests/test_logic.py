import pytest
from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


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
