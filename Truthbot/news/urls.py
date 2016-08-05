from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'news/$', views.post_list, name='postlist'),
    url(r'submit/$', views.submit_post, name='submitpost'),
    url(r'news/(?P<post_slug>[-\w]+)/$', views.post_view, name='postview'),
    url(r'news/(?P<post_slug>[-\w]+)/(?P<comment_pk>\d+)$', views.comment_perma, name='commentperma'),
    url(r'commentreply/(?P<comment_pk>\d+)/$', views.comment_reply, name='commentreply'),
    url(r'ajax/postvote/$', views.post_vote, name='postvote'),
    url(r'ajax/commentvote/$', views.comment_vote, name='commentvote'),
]
