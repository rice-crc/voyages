from django.contrib import admin
from voyages.apps.education.models import *

class LessonStandardInline(admin.TabularInline):
    model = LessonStandard
    extra = 6

class LessonPlanAdmin(admin.ModelAdmin):
    fields = ['text', 'author', 'grade_level', 'course', 'key_words', 'order', 'abstract']
    inlines = [LessonStandardInline]

admin.site.register(LessonPlan, LessonPlanAdmin)