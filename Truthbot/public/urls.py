from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^page/(?P<url>.+)$', views.article, name='publicarticle'),
]
