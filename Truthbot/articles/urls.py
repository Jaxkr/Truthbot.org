from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'article/(?P<organization_pk>\w+)/$', views.article_view, name='article'),
]
