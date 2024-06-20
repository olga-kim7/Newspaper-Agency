from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from agency.models import Redactor, Newspaper, Topic


# @login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()
    #
    # num_visits = request.session.get("num_visits", 0)
    # request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        # "num_visits": num_visits + 1,
    }

    return render(request, "agency/index.html", context=context)
