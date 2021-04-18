from __future__ import unicode_literals

from django.contrib import admin

from .models import ContentGroup, ContentPage


class ContentGroupAdmin(admin.ModelAdmin):
    fields = ["name"]


class ContentPageAdmin(admin.ModelAdmin):
    fields = ["title", "description", "order", "group"]
    list_display = ["title", "order", "group"]
    readonly_fields = ["order", "group"]
    search_fields = ["group__name"]

    # # Lock adding new items
    # def has_add_permission(self, request):
    #     return False


admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(ContentPage, ContentPageAdmin)
