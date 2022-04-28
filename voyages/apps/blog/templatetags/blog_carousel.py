from django import template

from ..models import PUBLISH_STATUS, Post, Tag

register = template.Library()

@register.inclusion_tag('blog/carousel.html', takes_context=True)
def show_last_posts(context):
    request = context['request']
    lang_code = request.LANGUAGE_CODE or "en"        
    
    return {"posts" : Post.objects.filter(status=PUBLISH_STATUS, language=lang_code).order_by('-created_on').exclude(tags__in = Tag.objects.filter(slug__in = ['author-profile','institution-profile']) )[:9]}
    
