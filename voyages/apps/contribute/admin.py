from django.contrib import admin

# Hide the Site and Group features
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from voyages.apps.contribute.models import AdminFaq
from voyages.apps.contribute.forms import AdminFaqAdminForm


class AdminFaqAdmin(admin.ModelAdmin):
    model = AdminFaq
    form = AdminFaqAdminForm
    fieldsets = (
        (None, {
            'fields': ('question',)
        }),
        ('Answer', {
            'fields': ('answer',)
        }),
    )
    search_fields = ['question', 'answer']



admin.site.register(AdminFaq, AdminFaqAdmin)

admin.site.unregister(Site)
admin.site.unregister(Group)


