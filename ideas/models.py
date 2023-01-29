import pickle
from django.db import models
from django.contrib.auth import get_user_model

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
