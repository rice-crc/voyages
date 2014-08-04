from django.contrib import admin
from .models import ContentGroup, ContentPage


class ContentGroupAdmin(admin.ModelAdmin):
    fields = ["name"]


class ContentPageAdmin(admin.ModelAdmin):
    fields = ["title", "description", "order", "group"]
    list_display = ["title", "order", "group"]
    search_fields = ["group__name"]

admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(ContentPage, ContentPageAdmin)