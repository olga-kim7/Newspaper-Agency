from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView

from agency.models import Redactor, Newspaper, Topic


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
    }

    return render(request, "agency/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "agency/topic_list.html"
    queryset = Topic.objects.all().order_by("name")
    paginate_by = 10


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    template_name = "agency/newspaper_list.html"
    queryset = Newspaper.objects.select_related("topic")
    context_object_name = "newspaper_list"
    paginate_by = 10


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    template_name = "agency/redactor_list.html"
    context_object_name = "redactor_list"
    queryset = Redactor.objects.all()
    paginate_by = 10


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor

#
# def login_view(request: HttpRequest) -> HttpResponse:
#     return render(request, "registration/login.html")
#
#
# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return render(request, "registration/logged_out.html")
