from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.views.generic import ListView

from agency.models import Newspaper, Redactor, Topic


def index(request: HttpRequest) -> HttpResponse:
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }
    return render(request, "agency/index.html", context=context)


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "agency/topic_list.html"
    paginate_by = 5


class NewspaperListView(LoginRequiredMixin, ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    template_name = "agency/newspaper_list.html"
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")


class RedactorListView(LoginRequiredMixin, ListView):
    model = Redactor
    paginate_by = 5
