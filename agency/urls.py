from django.urls import path

from . import views
from .views import (
    index,
    TopicListView,
    NewspaperListView,
    RedactorListView,
    RedactorDetailView, RedactorCreateView,
)

urlpatterns = [
    path("", index, name="index"),
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
    path(
        "redactor/<int:pk>/",
        RedactorDetailView.as_view(),
        name="redactor-detail",
    ),
    path(
        "redacor/create/",
        RedactorCreateView.as_view(),
        name="redactor-create",
    )
]

app_name = "agency"
