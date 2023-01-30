from ideas.models import Idea, Similarity
from itertools import combinations


def run_set_all_embeddings():
    ideas = Idea.objects.all()
    for idea in ideas:
        if not idea.embedding:
            idea.set_embedding()


def run_set_similarity_scores():
    ideas = Idea.objects.all()
    pairs = combinations(ideas, 2)
    for pair in pairs:
        sim = Similarity()
        sim.save()
        sim.ideas.set(pair)
        sim.set_score()
