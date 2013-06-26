from django.contrib import admin
from voyages.apps.help.models import *
from voyages.apps.help.forms import *

class GlossaryAdmin(admin.ModelAdmin):
    fields = ['term', 'description', ]
    search_fields = ('term', 'description')

class FaqAdminInline(admin.StackedInline):
    model = Faq
    form = FaqAdminForm
    extra = 6
    fieldsets = (
        (None, {
            'fields': ('question_order','question',)
        }),
        ('Answer', {
            'fields': ('answer',)
        }),
    )

class FaqCategoryAdmin(admin.ModelAdmin):
    fields = ['text', 'type_order']
    search_fields = ('text', 'type_order')


class FaqAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'question_order','question',)
        }),
        ('Answer', {
            'fields': ('answer',)
        }),
    )
    search_fields = ('question', 'answer',)
    form = FaqAdminForm
    list_display =  ['category', 'question_order', 'question',]
    list_display_links = ['question']
    list_editable = ['question_order']

admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(FaqCategory, FaqCategoryAdmin)
admin.site.register(Faq, FaqAdmin)
