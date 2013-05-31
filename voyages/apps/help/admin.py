from django.contrib import admin
from voyages.apps.help.models import *

class GlossaryAdmin(admin.ModelAdmin):
    fields = ['term', 'description', ]
    search_fields = ('term', 'description')

class FaqAdminInline(admin.TabularInline):
    model = Faq
    extra = 6

class FaqCategoryAdmin(admin.ModelAdmin):
    fields = ['text',]
    search_fields = ('text',)
    inlines = [FaqAdminInline]

class FaqAdmin(admin.ModelAdmin):
    fields = ['question', 'answer', 'category', 'question_order', ]
    search_fields = ('question', 'answer',)

admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(FaqCategory, FaqCategoryAdmin)
admin.site.register(Faq, FaqAdmin)