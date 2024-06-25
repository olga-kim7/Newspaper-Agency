from django.test import TestCase
from django.urls import reverse

from agency.forms import (
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm
)
from agency.models import Redactor, Newspaper, Topic


class PublicViewTests(TestCase):
    def setUp(self):
        self.index_url = reverse("agency:index")
        self.topic_list_url = reverse("agency:topic-list")
        self.topic_create_url = reverse("agency:topic-create")
        self.newspaper_list_url = reverse("agency:newspaper-list")
        self.redactor_list_url = reverse("agency:redactor-list")
        self.redactor_create_url = reverse("agency:redactor-create")

    def test_login_required(self):
        urls = [self.index_url,
                self.topic_list_url,
                self.topic_create_url,
                self.newspaper_list_url,
                self.redactor_list_url,
                self.redactor_create_url]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEquals(response.status_code, 200)


class IndexViewTests(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="test_driver",
            password="PASSWORD",
            years_of_experience=12
        )
        self.index_url = reverse("agency:index")
        self.user = Redactor.objects.create_user(
            username="test",
            password="password"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(self.index_url)

    def test_correctness_template(self):
        self.assertTemplateUsed(self.response, "agency/index.html")

    def test_redactor_counter_presents(self):
        num_redactors = Redactor.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            self.response.context["num_redactors"],
            num_redactors,
        )

    def test_redactor_newspaper_counter_presents(self):
        num_newspapers = Newspaper.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context["num_newspapers"], num_newspapers)

    def test_redactor_topic_counter_presents(self):
        num_topics = Topic.objects.count()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context["num_topics"], num_topics)

    def test_redactor_num_visits_counter_presents(self):
        self.assertEqual(self.response.context["num_visits"], 1)
        self.response = self.client.get(self.index_url)
        self.assertEqual(self.response.context["num_visits"], 2)


class TopicViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="test_name",
        )
        self.topic_url = reverse("agency:topic-list")
        self.user = Redactor.objects.create_user(
            username="test",
            password="password"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(self.topic_url)

    def test_correctness_template(self):
        self.assertTemplateUsed(self.response, "agency/topic_list.html")

    def test_search_fields_present(self):
        form = TopicSearchForm(data={"query": "test"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("agency:topic-list"), {"name": "test_name"}
        )
        self.assertContains(request, self.topic.name)


class NewspaperViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="test_name",
        )
        self.redactor = Redactor.objects.create_user(
            username="test",
            password="PASSWORD",
            years_of_experience=9
        )
        self.newspaper = Newspaper.objects.create(
            title="test_title",
            topic=self.topic,
            published_date="2020-02-01",
        )
        self.newspaper.publisher.add(self.redactor)
        self.client.force_login(self.redactor)
        self.newspaper_list = reverse("agency:newspaper-list")
        self.response = self.client.get(self.newspaper_list)

    def test_newspaper_search_present(self):
        form = NewspaperSearchForm(data={"query": "test_title"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("agency:newspaper-list"), {"title": "test_title"}
        )
        self.assertContains(request, self.newspaper.title)


class RedactorViewTests(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="test",
            password="PASSWORD",
            years_of_experience=9
        )
        self.topic = Topic.objects.create(
            name="test_name",
        )
        self.newspaper = Newspaper.objects.create(
            title="test_title",
            topic=self.topic,
            published_date="2020-02-01",
        )
        self.client.force_login(self.redactor)
        self.newspaper_list = reverse("agency:newspaper-list")
        self.response = self.client.get(self.newspaper_list)

    def test_redactor_search_present(self):
        form = RedactorSearchForm(data={"query": "test"})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)

    def test_get_queryset(self):
        request = self.client.get(
            reverse("agency:redactor-list"), {"username": "test"}
        )
        self.assertContains(request, self.redactor.username)

    def test_assign_unassign_redactor_to_newspaper(self):
        self.client.get(reverse("agency:newspaper-assign", args=[self.newspaper.pk]))
        self.newspaper.publisher.filter(pk=self.redactor.pk).exists()
        self.client.get(reverse("agency:newspaper-assign", args=[self.newspaper.pk]))
        self.newspaper.publisher.filter(pk=self.redactor.pk).exists()
        self.assertNotIn(self.redactor, self.newspaper.publisher.all())
