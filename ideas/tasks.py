from app.celery import app
from .models import Idea


@app.task
def find_similar_ideas(idea_id):
    Idea.objects.get(id=idea_id).get_similar_ideas()


@app.task
def run_set_embedding(idea_id):
    Idea.objects.get(id=idea_id).set_embedding()
