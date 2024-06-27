from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin


from agency.forms import (
    RedactorCreationForm,
    NewspaperForm,
    RedactorLicenseUpdateForm,
    NewspaperSearchForm,
    TopicSearchForm,
    RedactorSearchForm
)
from agency.models import Redactor, Newspaper, Topic


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "agency/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    paginate_by = 10
    template_name = "agency/topic_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("query", "")
        context["search_form"] = TopicSearchForm(
            initial={"query": name}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all().order_by("name")
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["query"])
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    template_name = "agency/topic_form.html"
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 10
    template_name = "agency/newspaper_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("query", "")
        contex["search_form"] = NewspaperSearchForm(
            initial={"query": title}
        )
        return contex

    def get_queryset(self):
        queryset = Newspaper.objects.select_related("topic")
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["query"])
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "agency/newspaper_detail.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 10
    context_object_name = "redactor_list"
    template_name = "agency/redactor_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("query", "")
        context["search_form"] = RedactorSearchForm(
            initial={"query": username}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["query"]
            )
        return queryset


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorLicenseUpdateForm


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("publisher__topic")
    paginate_by = 10
    template_name = "agency/redactor_detail.html"


class AssignUserToNewspaperView(LoginRequiredMixin, View):

    def post(self, request, pk):
        newspaper = Newspaper.objects.get(pk=pk)
        if request.user not in newspaper.publisher.all():
            newspaper.publisher.add(request.user)
        else:
            newspaper.publisher.remove(request.user)
        return (HttpResponseRedirect
                (reverse_lazy("agency:newspaper-detail", kwargs={"pk": pk})))
