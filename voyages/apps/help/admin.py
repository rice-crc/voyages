from django.contrib import admin
from voyages.apps.help.models import Glossary

class GlossaryAdmin(admin.ModelAdmin):
    fields = ['term', 'description', ]
    search_fields = ('term', 'description')

admin.site.register(Glossary, GlossaryAdmin)
