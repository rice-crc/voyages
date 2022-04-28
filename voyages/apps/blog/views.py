from django.views import generic
from .models import PUBLISH_STATUS, Post, Tag
from .models import Author
from .models import Institution


class PostList(generic.ListView):    
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        lang_code = self.request.LANGUAGE_CODE or "en"
        if self.kwargs.get('tag') is None:
            return Post.objects.filter(status=PUBLISH_STATUS, language=lang_code).order_by('-created_on').exclude(tags__in = Tag.objects.filter(slug__in = ['author-profile','institution-profile']) )
        return Post.objects.filter(status=PUBLISH_STATUS, language=lang_code, tags__slug__in=[self.kwargs['tag']]).order_by('-created_on')


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self):
        if 'pk' in self.kwargs:
            return Post.objects.get(pk=self.kwargs['pk'])
        slug = self.kwargs.get('slug')
        if slug is not None:
            lang_code = self.request.LANGUAGE_CODE or "en"
            matches = Post.objects.filter(slug=slug,language=lang_code)[:2]
            if len(matches) == 1:
                return matches[0]
            if lang_code != "en":
                # Fallback to the English language if the translation is not
                # found for this slug.
                matches = Post.objects.filter(slug=slug,language="en")[:2]
            if len(matches) == 1:
                return matches[0]
        return None

class AuthorBio(generic.DetailView):
    #lang_code = self.request.LANGUAGE_CODE or "en"
    model = Author
    template_name = 'blog/author_bio.html'

    def get_context_data(self, **kwargs):
        
        context = super(AuthorBio, self).get_context_data(**kwargs)

        lang_code = self.request.LANGUAGE_CODE or "en"

        if 'pk' in self.kwargs:        
            author = Author.objects.get(pk=self.kwargs['pk'])
            posts = author.post_set.exclude(slug=author.slug).filter(language=lang_code) 
            
            profile = Post.objects.filter(slug= author.slug, language=lang_code)[:2]
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
            #posts = institution.post_set.exclude(slug=institution.slug).filter(language=lang_code) 
            
            profile = Post.objects.filter(slug= institution.slug, language=lang_code)[:2]
            if len(profile) == 1:
                context['profile'] = profile[0].content
            else:
                context['profile'] = ''

            #context['posts'] = posts
            

        return context

class AuthorList(generic.ListView):    
    template_name = 'blog/authors.html'
    paginate_by = 5

    def get_queryset(self):
        return Author.objects.order_by('name')
        

class InstitutionList(generic.ListView):    
    template_name = 'blog/institutions.html'
    paginate_by = 5

    def get_queryset(self):
        return Institution.objects.order_by('name')

