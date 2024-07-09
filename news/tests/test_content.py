import pytest
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(news_custom_date, client):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context["object_list"]
    news_count = object_list.count()
    assert news_count == 10


@pytest.mark.django_db
def test_news_order(news_custom_date, client):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context["object_list"]
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.django_db
def test_comments_order(news, author_client, comments):
    url = reverse("news:detail", args=(news.id,))
    response = author_client.get(url)
    news = response.context["news"]
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse("news:detail", args=(news.id,))
    response = client.get(url)
    assert "form" not in response.context


def test_authorized_client_has_form(author_client, news):
    url = reverse("news:detail", args=(news.id,))
    response = author_client.get(url)
    assert "form" in response.context
    assert isinstance(response.context["form"], CommentForm)
