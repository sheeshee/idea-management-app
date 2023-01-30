import pickle
from django.db import models
from django.contrib.auth import get_user_model
from sentence_transformers import util

from nlp import language_model

User = get_user_model()

# Create your models here.
class Idea(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", blank=True)
    embedding = models.BinaryField(blank=True)

    def __str__(self):
        return self.title

    def get_text(self):
        return self.title + " " + self.body

    def calculate_embedding(self):
        return language_model.encode(self.get_text(), convert_to_numpy=True)

    def set_embedding(self):
        array = self.calculate_embedding()
        self.embedding = pickle.dumps(array)
        self.save()

    def get_embedding(self):
        if self.embedding:
            return pickle.loads(self.embedding)
        else:
            return None

    def get_most_similar(self):
        similarity = self.similarity_set.order_by("-score").first()
        idea = similarity.ideas.filter(~models.Q(id=self.id)).first()
        return idea


class Similarity(models.Model):

    class Meta:
        verbose_name_plural = "Similarities"

    score = models.FloatField(null=True)
    ideas = models.ManyToManyField(Idea)

    def calculate(self):
        embeddings = []
        for idea in self.ideas.all():
            idea.set_embedding()
            embeddings.append(idea.get_embedding())
        assert len(embeddings) == 2, "There can only be two ideas per Similarity object"
        assert all([e is not None for e in embeddings]), "Embeddings for both objects must exist"
        return float(util.cos_sim(embeddings[0], embeddings[1]))

    def set_score(self):
        self.score = self.calculate()
        self.save()
