# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.shortcuts import render_to_response
from voyages.apps.education.models import *

def lessonplan(request):
    """
    Display the lesson plan page in the Education section
    ** Context **
    ``RequestContext``
    ``mymodel``
        An instance of :model:`education:LessonPlan`
        requires :model:`education:LessonStandard`
        requires :model:`education:LessonStandardType`
        requires :model:`education:LessonPlanFile`
    
    ** Template **
    :template:`education/lesson-plans.html`
    """
    
    lesson_plan_list = []
    # Iterate and retrieve all nested submenus
    for lesson in LessonPlan.objects.order_by('order'):
        sub_lesson = []
        sub_download = []
      
        for std_type in LessonStandardType.objects.all():
            text_list = LessonStandard.objects.filter(lesson=lesson.id).filter(type=std_type)
            if len(text_list) != 0:
                sub_lesson.append({'type' : std_type.type, 'text' : text_list})
        
        lesson_plan_list.append({'lesson' : lesson, 'standard' : sub_lesson, 'download' : LessonPlanFile.objects.filter(lesson=lesson.id)})
    
    return render_to_response('education/lesson-plans.html', {"lesson_plans" : lesson_plan_list},
                              context_instance=RequestContext(request));
                            