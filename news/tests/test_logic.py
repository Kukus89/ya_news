from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.tests.conftest import COMMENT_TEXT


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse("news:detail", args=(news.id,))
    client.post(url, data=form_data)
    comment_count = Comment.objects.all().count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, form_data):
    url = reverse("news:detail", args=(news.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f"{url}#comments")
    comment_count = Comment.objects.all().count()
    comment = Comment.objects.get()

    assert comment_count == 1
    assert comment.text == form_data["text"]
    assert comment.news == news
    assert comment.author.username == "author"


def test_user_cant_use_bad_words(author_client, news, form_data):
    url = reverse("news:detail", args=(news.id,))
    response = author_client.post(url, data={"text": BAD_WORDS[0]})
    comment_count = Comment.objects.all().count()
    assert comment_count == 0
    assertFormError(response, form="form", field="text", errors=WARNING)


@pytest.mark.django_db
def test_author_can_delete_comment(comment, author_client):
    delete_url = reverse("news:delete", args=(comment.id,))
    news_url = reverse("news:detail", args=(comment.id,))
    comment_url = news_url + "#comments"
    response = author_client.delete(delete_url)
    comment_count = Comment.objects.all().count()
    assertRedirects(response, comment_url)
    assert comment_count == 0


@pytest.mark.django_db
def test_author_cant_delete_another_author_comment(comment, not_author_client):
    delete_url = reverse("news:delete", args=(comment.id,))
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.all().count()
    assert comment_count == 1


@pytest.mark.django_db
def test_author_can_edit_comment(comment, author_client, form_data):
    edit_url = reverse("news:edit", args=(comment.id,))
    news_url = reverse("news:detail", args=(comment.id,))
    comment_url = news_url + "#comments"
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, comment_url)
    comment.refresh_from_db()
    assert comment.text == form_data["text"]


@pytest.mark.django_db
def test_author_cant_edit_comment_of_another_author(
    comment, not_author_client, form_data
):
    edit_url = reverse("news:edit", args=(comment.id,))
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
