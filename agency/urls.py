from django.contrib import admin
from django.urls import path

from agency.views import (
    index,
    TopicListView,
    NewspaperListView,
    RedactorListView,
    NewspaperDetailView,
    TopicDetailView,
    RedactorDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path("redactor/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),

]

app_name = "agency"
