from django.views.generic import CreateView, ListView, DetailView
from django.db import transaction
from django.forms import ModelForm
from django.urls import reverse_lazy
from ideas.models import Idea
from ideas.tasks import run_set_similarities

# Create your views here.
class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ["title", "body"]


class CreateIdea(CreateView):
    model = Idea
    form_class = IdeaForm
    success_url = reverse_lazy("index")

    @transaction.atomic
    def form_valid(self, form):
        form.instance.owner = self.request.user
        # save the form so that pk's can be defined for the many-to-many field
        obj = form.save()
        parent_id_list = self.request.POST.get("related")
        if parent_id_list is not None:
            if isinstance(parent_id_list, str):
                parent_id_list = [int(parent_id_list)]
            form.instance.related.set(
                [Idea.objects.get(pk=pk) for pk in parent_id_list]
            )
        response = super().form_valid(form)
        run_set_similarities.delay(obj.id)
        return response


class ListIdeas(ListView):
    model = Idea


class DetailIdea(DetailView):
    model = Idea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inspired_idea_form"] = IdeaForm()
        return context
