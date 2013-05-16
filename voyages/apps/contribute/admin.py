from django.contrib import admin
from voyages.apps.contribute.models import *

#class LessonPlanFileAdmin(admin.ModelAdmin):
#    fields = ['file', 'filetitle',]
#    search_fields = ('filetitle',)
#
#admin.site.register(LessonPlanFile, LessonPlanFileAdmin)

class DownloadFileAdmin(admin.ModelAdmin):
    fields = ['file', 'filetitle', ]

admin.site.register(DownloadFile, DownloadFileAdmin)
