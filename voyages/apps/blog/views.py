from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    #queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs.get('tag') is None:
            return Post.objects.filter(status=1).order_by('-created_on')
        else:
            return Post.objects.filter(status=1,tags__name__in=[self.kwargs['tag']]).order_by('-created_on')
        #return CandidateNote.objects.filter(user__username=self.kwargs['username'])


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'