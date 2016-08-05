from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^orginfo/$', views.get_org_info, name='getorginfo'),
    url(r'^getposts/$', views.get_posts, name='getposts'),
]
