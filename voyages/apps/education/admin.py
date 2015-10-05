from django.contrib import admin
from voyages.apps.education.models import *

class LessonStandardInline(admin.TabularInline):
    model = LessonStandard
    extra = 6

class FileDownloadInline(admin.TabularInline):
    model = LessonPlanFile
    extra = 3

class LessonPlanAdmin(admin.ModelAdmin):
    fields = ['text', 'author', 'grade_level', 'course', 'key_words', 'order', 'abstract']
    inlines = [LessonStandardInline, FileDownloadInline,]
    search_fields = ('text','author', 'grade_level', 'course', 'key_words',  'abstract')
    list_display=  ['order', 'text', 'author', 'key_words', 'grade_level', 'course']
    list_display_links = ['text']
    list_editable = ['order']
    
class LessonStandardTypeAdmin(admin.ModelAdmin):
    fields = ['type',]
    search_fields = ('type',)

class DownloadFileAdmin(admin.ModelAdmin):
    fields = ['file', 'filetitle', ]

admin.site.register(LessonPlan, LessonPlanAdmin)
admin.site.register(LessonStandardType, LessonStandardTypeAdmin)