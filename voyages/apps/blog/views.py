from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Post
from .models import Author
from .models import Institution

class PostList(generic.ListView):    
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs.get('tag') is None:
            return Post.objects.filter(status=1).order_by('-created_on')
        else:            
            return Post.objects.filter(status=1,tags__slug__in=[self.kwargs['tag']]).order_by('-created_on')        


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class AuthorBio(generic.DetailView):
    model = Author
    template_name = 'blog/author_bio.html'

class InstitutionDetail(generic.DetailView):
    model = Institution
    template_name = 'blog/institution_detail.html'

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

