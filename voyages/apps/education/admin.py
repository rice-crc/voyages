from django.contrib import admin
from voyages.apps.education.models import LessonStandard, LessonPlan
from voyages.apps.contribute.models import LessonPlanFile

class LessonStandardInline(admin.TabularInline):
    model = LessonStandard
    extra = 6

class FileDownloadInline(admin.TabularInline):
    model = LessonPlanFile
    extra = 3

class LessonPlanAdmin(admin.ModelAdmin):
    fields = ['text', 'author', 'grade_level', 'course', 'key_words', 'order', 'abstract']
    inlines = [LessonStandardInline, FileDownloadInline,]
    
admin.site.register(LessonPlan, LessonPlanAdmin)