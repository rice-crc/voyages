from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 5


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'