from django.contrib.syndication.views import Feed
from .models import Post
from django.urls import reverse

class LatestPostEntries (Feed):
    title = "Voyages blog"
    link = "/blog/feed"
    description = "Last posts from the blog"

    def get_object(self, request, language = 'en'):
        return language

    def items(self,obj):        
        # TODO: detect the language needed from the feed.
        return Post.objects.filter(language=obj).order_by('-created_on')[:20]

    def item_title(self,item):
        return item.title

    def item_description(self,item):
        return item.title

    def item_link(self,item):
        return reverse('blog:post_detail', args=[item.slug,item.language])
    


