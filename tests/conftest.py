from django.test import Client
import pytest
import factory
from pytest_factoryboy import register


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    username = factory.Faker("email")
    id = factory.Sequence(lambda x: x)


@register
class IdeaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ideas.Idea"

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("paragraph", nb_sentences=3)
    owner = factory.SubFactory(UserFactory)
