from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'article/(?P<url>.+)/$', views.article_view, name='article'),
]
