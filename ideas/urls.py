from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListIdeas.as_view(), name="index"),
    path("new", views.CreateIdea.as_view(), name="new"),
]
