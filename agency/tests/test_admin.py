from django.test import TestCase, Client
from django.urls import reverse

from agency.models import Redactor, Topic, Newspaper


class AdminTestCase(TestCase):
    def setUp(self):
        self.admin = Redactor.objects.create_superuser(
            "test_admin",
            "EMAIL",
            "0000"
        )
        self.client = Client()
        self.client.force_login(self.admin)
        self.topic = Topic.objects.create(
            name="test_name",
        )
        self.redactor = Redactor.objects.create_user(
            username="test",
            password="PASSWORD",
            years_of_experience="14"
        )
        self.newspaper = Newspaper.objects.create(
            title="test_title",
            topic=self.topic,
            published_date="2024-06-25"
        )
        self.newspaper.publisher.add(self.redactor)

    def test_newspaper_list_has_filter(self):
        url = reverse("admin:agency_newspaper_changelist")
        response = self.client.get(url)
        self.assertContains(response, "topic")

    def test_newspaper_list_has_searching(self):
        url = reverse("admin:agency_newspaper_changelist")
        response = self.client.get(url)
        self.assertContains(response, "title")

    def test_redactor_years_of_experience(self):
        url = reverse("admin:agency_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_change_years_of_experience(self):
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_assign_to_newspaper(self):
        url = reverse("agency:newspaper-assign", args=[self.newspaper.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        newspaper = Newspaper.objects.get(pk=self.newspaper.pk)

        self.assertTrue(
            newspaper.publisher.filter(pk=self.redactor.pk).exists()
        )
