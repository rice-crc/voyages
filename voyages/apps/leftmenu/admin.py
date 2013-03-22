from voyages.apps.leftmenu.models import LeftMenuItem
from django.contrib import admin

class LeftMenuAdmin(admin.ModelAdmin):
    fields = ['text', 'orderNum','url', 'parent']

admin.site.register(LeftMenuItem, LeftMenuAdmin)
