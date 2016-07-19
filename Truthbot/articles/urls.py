from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'article/(?P<url>.+)/$', views.article_view, name='article'),
    url(r'id/(?P<article_pk>\d+)/new-review/$', views.article_create_review, name='articlecreatereview'),
]
