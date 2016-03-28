from django.conf.urls import url
from django.views.generic import TemplateView
from voyages.apps.contribute import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^guidelines', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),

    url(r'^thanks', TemplateView.as_view(template_name='contribute/thanks.html'), name='thanks'),

    url(r'^delete_voyage', views.delete, name='delete_voyage'),

    url(r'^delete_review/(?P<contribution_id>\d+)', views.delete_review, name='delete_review'),

    url(r'^places_ajax', views.get_places, name='places_ajax'),

    url(r'^voyage_ajax', views.get_voyage_by_id, name='voyage_ajax'),

    url(r'interim/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)',
        views.interim, name='interim'),

    url(r'interim_commit/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)',
        views.interim_commit, name='interim_commit'),

    url(r'interim_summary/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)',
        views.interim_summary, name='interim_summary'),

    url(r'interim_summary/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)/(?P<mode>reviewer)',
        views.interim_summary, name='interim_summary_reviewer'),

    url(r'interim_summary/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)/(?P<mode>editor)',
        views.interim_summary, name='interim_summary_editor'),

    url(r'edit_voyage', views.edit, name='edit_voyage'),

    url(r'merge_voyages', views.merge, name='merge_voyages'),

    url(r'new_voyage', views.new_voyage, name='new_voyage'),

    url(r'editor_main', views.editor_main, name='editor_main'),

    url(r'review_request/(?P<review_request_id>\d+)',
        views.review_request, name='review_request'),
    url(r'reply_review_request', views.reply_review_request, name='reply_review_request'),
    url(r'review/(?P<review_request_id>\d+)', views.review, name='review'),

    url(r'json_pending_requests', views.get_pending_requests, name='json_pending_requests'),
    url(r'json_reviewers', views.get_reviewers, name='json_reviewers'),

    url(r'post_review_request', views.post_review_request, name='post_review_request'),
    url(r'post_archive_review_request', views.post_archive_review_request, name='post_archive_review_request')
    ]

