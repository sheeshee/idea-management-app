from ideas.models import Idea


def run_set_all_embeddings():
    ideas = Idea.objects.all()
    for idea in ideas:
        if not idea.embedding:
            idea.set_embedding()
