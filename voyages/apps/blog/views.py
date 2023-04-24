from django.views import generic
from .models import PUBLISH_STATUS,DRAFT_STATUS, Post, Tag
from .models import Author
from .models import Institution

from django import template
register = template.Library()

class PostList(generic.ListView):
    template_name = 'blog/index.html'
    paginate_by = 12

    base_query = Post.objects.select_related()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_override'] = self.kwargs.get('title_override')
        tag_slug = self.kwargs.get('tag')
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            if tag and tag.intro:
                context['intro'] = tag.intro
        return context
	
    def get_queryset(self):
        lang_code = self.request.LANGUAGE_CODE or "en"
        q = self.__class__.base_query
        if self.request.resolver_match.url_name == 'news':
            return q.filter(status=PUBLISH_STATUS, language=lang_code, tags__slug__in=['news']).order_by('-created_on').order_by('-created_on')
        if self.kwargs.get('tag') is None:
            return q.filter(status=PUBLISH_STATUS, language=lang_code).order_by('-created_on').exclude(tags__in = Tag.objects.filter(slug__in = ['author-profile','institution-profile']) )
        return q.filter(status=PUBLISH_STATUS, language=lang_code, tags__slug__in=[self.kwargs['tag']]).order_by('-created_on')



class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.object:
            isNews = self.object.tags.filter(slug__in =['news','front-page'] ).count() > 0
            context['is_news'] = isNews

        return context

    def get_object(self):
        
        if 'pk' in self.kwargs:
            post = Post.objects.get(pk=self.kwargs['pk'])            
            return  post

        slug = self.kwargs.get('slug')
        language_param = self.kwargs.get('language')
        
        if slug is not None:
            lang_code = self.request.LANGUAGE_CODE or "en"

            if language_param is not None:
                lang_code = language_param
            
            matches = Post.objects.filter(status=PUBLISH_STATUS, slug=slug,language=lang_code)[:2]            
            if len(matches) == 1:
                return matches[0]
            if lang_code != "en":
                # Fallback to the English language if the translation is not
                # found for this slug.
                matches = Post.objects.filter(status=PUBLISH_STATUS, slug=slug,language="en")[:2]
            if len(matches) == 1:
                return matches[0]
        return None

class AuthorBio(generic.DetailView):
    
    model = Author
    template_name = 'blog/author_bio.html'

    def get_context_data(self, **kwargs):
        
        context = super(AuthorBio, self).get_context_data(**kwargs)

        lang_code = self.request.LANGUAGE_CODE or "en"

        if 'pk' in self.kwargs:        
            author = Author.objects.get(pk=self.kwargs['pk'])
            posts = author.post_set.exclude(slug=author.slug).filter(status=PUBLISH_STATUS,language=lang_code)
            
            profile = Post.objects.filter(status=PUBLISH_STATUS, slug= author.slug, language=lang_code)[:2]
            if len(profile) == 1:
                context['profile'] = profile[0].content
            else:
                context['profile'] = ''

            context['posts'] = posts
            

        return context


class InstitutionDetail(generic.DetailView):
    model = Institution
    template_name = 'blog/institution_detail.html'

    def get_context_data(self, **kwargs):
        
        context = super(InstitutionDetail, self).get_context_data(**kwargs)

        lang_code = self.request.LANGUAGE_CODE or "en"

        if 'pk' in self.kwargs:        
            institution = Institution.objects.get(pk=self.kwargs['pk'])
            
            
            profile = Post.objects.filter(status=PUBLISH_STATUS, slug= institution.slug, language=lang_code)[:2]
            if len(profile) == 1:
                context['profile'] = profile[0].content
            else:
                context['profile'] = ''

        return context

class AuthorList(generic.ListView):    
    template_name = 'blog/authors.html'
    paginate_by = 12

    def get_queryset(self):
        return Author.objects.order_by('name')
        

class InstitutionList(generic.ListView):    
    template_name = 'blog/institutions.html'
    paginate_by = 12

    def get_queryset(self):
        return Institution.objects.order_by('name')

