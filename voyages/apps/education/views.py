# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader
from django.views.generic.simple import direct_to_template

def lessonplan(request):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    lessons = LessonPlan.objects.order_by('order')
    standards = LessonStandard.objects.all()
    
    return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"lesson_plans" : lessons}));
                            