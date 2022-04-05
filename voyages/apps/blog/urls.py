from . import views
#from django.urls import path
from django.conf.urls import url

from .feeds import LatestPostEntries


feeds = {
    'posts':  LatestPostEntries
}

urlpatterns = [
    
    url(r'^$', views.PostList.as_view(), name='blog'),
    url(r'^authors/$',views.AuthorList.as_view(),name='authors'),        
    url(r'^institutions/$',views.InstitutionList.as_view(),name='institutions'),        
    url(r'^institution/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.InstitutionDetail.as_view(), name='institution_detail'), 
    url(r'^author/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.AuthorBio.as_view(), name='author_bio'), 
    url('(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post_detail'), 
    url(r'^tag/(?P<tag>[-\w]+)$',views.PostList.as_view(),name='tag'),        
    url(r'^feed/$', LatestPostEntries()),
]