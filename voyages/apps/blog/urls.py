from . import views
#from django.urls import path
from django.conf.urls import url

urlpatterns = [
    
    url(r'^$', views.PostList.as_view(), name='blog'),
    url('(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post_detail'), 
    url(r'^tag/(?P<tag>[-\w]+)$',views.PostList.as_view(),name='tag')
]