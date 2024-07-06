import pytest
from django.test.client import Client
from news.models import Comment, News
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

COMMENT_TEXT = "Test comment"


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create_user(username='not_author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Test News',
        text="Test News"
    )


@pytest.fixture
def news_custom_date():
    today = datetime.today()
    News.objects.bulk_create(News(
        title='Заголовок новости',
        text='Тестовый текст',
        date=today - timedelta(days=index)
    ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT
    )


@pytest.fixture
def comment_id(comment):
    return (comment.id,)


@pytest.fixture
def comments(news, author):
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=COMMENT_TEXT
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data(news):
    return {
        'text': 'Test comment new'
    }
