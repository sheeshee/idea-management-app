from django.test import Client
import pytest
import factory
from pytest_factoryboy import register

from ideas.models import Similarity


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


@register(_name="idea_with_related")
class IdeaWithRelatedIdea(IdeaFactory):
    @factory.post_generation
    def set_related(obj, create, extracted, **kwargs):
        other_idea = IdeaFactory()
        obj.related.set([other_idea])


@pytest.fixture
def ideas_list():
    return IdeaFactory.create_batch(3)


@pytest.fixture
def similarity(ideas_list):
    sim = Similarity()
    sim.save()
    sim.ideas.set(ideas_list[0:2])
    return sim
