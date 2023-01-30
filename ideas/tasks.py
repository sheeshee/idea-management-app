from app.celery import app
from django.db.models import Q
from .models import Idea, Similarity


@app.task
def run_set_similarities(idea_id):
    base = Idea.objects.get(id=idea_id)
    base.set_embedding()
    ideas = Idea.objects.filter(~Q(id=idea_id)).all()
    for idea in ideas:
        sim = Similarity()
        sim.save()
        sim.ideas.set([base, idea])
        sim.set_score()
