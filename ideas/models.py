from django.db import models
from django.core import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Idea(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.title
