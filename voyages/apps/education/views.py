# Create your views here.
from django.shortcuts import render
from voyages.apps.education.models import *


def lessonplan(request):
    """
    Display :class:`~voyages.apps.education.models.LessonPlan` modles
    in the lesson plan page in the Education section
    """
    lesson_plan_list = []
    for lesson in LessonPlan.objects.order_by('order'):
        sub_lesson = []
        sub_download = []
      
        for std_type in LessonStandardType.objects.all():
            text_list = LessonStandard.objects.filter(lesson=lesson.id,type=std_type)
            if len(text_list) != 0:
                sub_lesson.append({'type': std_type.type, 'text' : text_list})
        
        lesson_plan_list.append({'lesson': lesson, 'standard': sub_lesson,
                                 'download': LessonPlanFile.objects.filter(lesson=lesson.id)})
    
    return render(request, 'education/lesson-plans.html', {"lesson_plans": lesson_plan_list})