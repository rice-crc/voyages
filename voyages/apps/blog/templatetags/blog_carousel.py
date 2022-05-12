from django import template

from ..models import PUBLISH_STATUS, Post, Tag

register = template.Library()

@register.inclusion_tag('blog/carousel.html', takes_context=True)
def show_last_posts(context, max_results = None):
    request = context['request']
    lang_code = request.LANGUAGE_CODE or "en"        
    
    if max_results is None:
        try:
            from voyages.localsettings import CAROUSEL_MAX_POSTS
            max_results = CAROUSEL_MAX_POSTS
        except Exception as e:
            max_results = 9
            
    return {"posts" : Post.objects.filter(status=PUBLISH_STATUS, language=lang_code, tags__slug__in=['front-page']).order_by('-created_on').exclude(tags__in = Tag.objects.filter(slug__in = ['author-profile','institution-profile']) )[:max_results]}
    
