from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField("Redactor", related_name="publisher")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)
