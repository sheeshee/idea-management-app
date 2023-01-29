from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from ideas.models import Idea

# Create your views here.
class CreateIdea(CreateView):
    model = Idea
    fields = ["title", "body"]
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListIdeas(ListView):
    model = Idea
