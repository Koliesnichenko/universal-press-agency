from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView

from agency.forms import (
    RedactorCreationForm,
    RedactorYearsOfExperienceCreationForm,
    TopicSearchForm,
    NewspaperCreationForm,
    NewspaperUpdateForm,
    NewspaperSearchForm,
    RedactorSearchForm,
)
from agency.models import Newspaper, Redactor, Topic


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "agency/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_newspapers"] = Newspaper.objects.count()
        context["num_redactors"] = Redactor.objects.count()
        context["num_topics"] = Topic.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits + 1

        return context


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "agency/topic_list.html"
    paginate_by = 5

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    template_name = "agency/newspaper_list.html"
    paginate_by = 5

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("topics", "publishers")
        title = self.request.GET.get("title", "")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperCreationForm
    success_url = reverse_lazy("agency:newspaper-list")

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()
        form.save_m2m()
        return super().form_valid(form)


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperUpdateForm
    success_url = reverse_lazy("agency:newspaper-list")

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()
        form.save_m2m()
        return super().form_valid(form)


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "agency/newspaper_detail.html"
    queryset = Newspaper.objects.prefetch_related("publishers", "topics")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("newspapers__topics")
        username = self.request.GET.get("username", "")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__topics")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorYearOfExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsOfExperienceCreationForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")


class ToggleAssignToNewspaperView(LoginRequiredMixin, View):
    def get(self, request, pk):
        redactor = get_object_or_404(Redactor, id=request.user.id)
        newspaper = get_object_or_404(Newspaper, id=pk)

        if redactor.newspapers.filter(id=newspaper.id).exists():
            redactor.newspapers.remove(newspaper)
        else:
            redactor.newspapers.add(newspaper)

        return HttpResponseRedirect(reverse_lazy("agency:newspaper-detail", kwargs={"pk": pk}))
