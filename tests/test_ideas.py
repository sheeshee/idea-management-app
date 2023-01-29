from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
import pytest
from conftest import IdeaFactory
from ideas.models import Idea
from tests.conftest import IdeaFactory
import numpy as np


User = get_user_model()


@pytest.fixture
def ideas_list():
    return IdeaFactory.create_batch(3)


@pytest.fixture
def ideas_list_view(client):
    return client.get("/ideas/")


@pytest.fixture
def idea_json():
    return model_to_dict(IdeaFactory.build(), exclude=("id", "owner"))


@pytest.fixture
def post_idea(authenticated_client, idea_json):
    return authenticated_client.post("/ideas/new", idea_json)


@pytest.fixture
def post_inspired_idea(authenticated_client, idea, idea_json):
    idea_json["related"] = [idea.pk]
    return authenticated_client.post("/ideas/new", idea_json)


@pytest.fixture
def get_idea(authenticated_client, idea):
    return authenticated_client.get(f"/ideas/{idea.pk}")


@pytest.fixture
def get_idea_with_related(authenticated_client, idea_with_related):
    return authenticated_client.get(f"/ideas/{idea_with_related.pk}")


@pytest.mark.django_db
def test_list_view_has_title(ideas_list_view):
    assert b"Existing Ideas" in ideas_list_view.content


@pytest.mark.django_db
def test_list_view_shows_ideas_in_db(ideas_list, ideas_list_view):
    for idea in ideas_list:
        assert idea.title in str(ideas_list_view.content)


@pytest.mark.django_db
def test_post_idea_response_302(post_idea):
    assert post_idea.status_code == 302


@pytest.mark.django_db
def test_post_idea_db_updated(post_idea, idea_json):
    idea_db = model_to_dict(
        Idea.objects.get(title=idea_json["title"]),
        exclude=("id", "owner"),
    )
    assert idea_db == idea_json


@pytest.mark.django_db
def test_post_idea_owner_set(post_idea):
    idea = Idea.objects.last()
    assert isinstance(idea.owner, User)


@pytest.mark.django_db
def test_detail_view_200(get_idea):
    assert get_idea.status_code == 200


@pytest.mark.django_db
def test_detail_view(get_idea, idea):
    assert idea.title in str(get_idea.content)


@pytest.mark.django_db
def test_detail_view_shows_related_ideas(get_idea_with_related, idea_with_related):
    related_idea = idea_with_related.related.first()
    assert related_idea.title in str(get_idea_with_related.content)


@pytest.mark.django_db
def test_create_inspired_idea_302(post_inspired_idea):
    assert post_inspired_idea.status_code == 302


@pytest.mark.django_db
def test_create_inspired_idea_db_updated(post_inspired_idea, idea_json):
    new_idea = Idea.objects.get(title=idea_json["title"])
    related_ids = list(new_idea.related.all().values_list("pk", flat=True))
    assert related_ids == idea_json["related"]


@pytest.mark.django_db
def test_set_embedding(idea):
    idea.set_embedding()
    assert idea.embedding is not None


@pytest.mark.django_db
def test_get_embedding(idea):
    idea.set_embedding()
    embedding = idea.get_embedding()
    assert isinstance(embedding, np.ndarray)
