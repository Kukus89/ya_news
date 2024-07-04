from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest
from news.forms import CommentForm
from news.models import Comment


@pytest.mark.django_db
def test_news_count(news_custom_date, client):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == 10


@pytest.mark.django_db
def test_news_order(news_custom_date, client):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.django_db
def test_comments_order(comment, author_client):
    url = reverse("news:detail", args=(comment.news.id,))
    print(Comment.objects.count())
    # object_list = response.context['object_list']
    # all_dates = [news.date for news in object_list]
    # sorted_dates = sorted(all_dates, reverse=True)
    # assert sorted_dates == all_dates
