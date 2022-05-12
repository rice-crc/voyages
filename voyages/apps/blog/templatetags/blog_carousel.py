from django import template

from ..models import PUBLISH_STATUS, Post, Tag

register = template.Library()

@register.inclusion_tag('blog/carousel.html', takes_context=True)
def show_last_posts(context, maxresults = 9):
    request = context['request']
    lang_code = request.LANGUAGE_CODE or "en"        

    print("max results")
    print(maxresults)

    print('context here')
    print(context)

    
    
    STATIC_URL = context['STATIC_URL']
    
    return {"STATIC_URL":STATIC_URL,"posts" : Post.objects.filter(status=PUBLISH_STATUS, language=lang_code, tags__slug__in=['news']).order_by('-created_on').exclude(tags__in = Tag.objects.filter(slug__in = ['author-profile','institution-profile']) )[:maxresults]}
    
