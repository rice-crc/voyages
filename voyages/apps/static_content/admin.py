from django.contrib import admin
from .models import ContentGroup, ContentPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class ContentGroupAdmin(admin.ModelAdmin):
    fields = ["name"]


class ContentPageAdmin(admin.ModelAdmin):
    fields = ["title", "description", "order", "group"]
    list_display = ["title", "order", "group"]
    readonly_fields = ["order", "group"]
    search_fields = ["group__name"]

    # Lock adding new items
    def has_add_permission(self, request):
        return False



# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'registration_required',
                'template_name',
            ),
        }),
    )

# Group remains closed in the admin
# admin.site.register(ContentGroup, ContentGroupAdmin)
admin.site.register(ContentPage, ContentPageAdmin)


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
