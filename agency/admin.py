from django.contrib import admin
from .models import Topic, Newspaper, Redactor


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ("topic",)

admin.site.register(Topic)
admin.site.register(Redactor)
