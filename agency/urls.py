from django.urls import path

from . import views
from .views import (
    TopicListView,
    NewspaperListView, RedactorListView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list",
    ),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list",
    ),
    path(
        "redactors/",
        RedactorListView.as_view(),
        name="redactor-list",
    ),
]

app_name = "agency"
