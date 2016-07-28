from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

# just using stock django shit for now
urlpatterns = [
    url(r'^cast/$', views.cast_vote, name='castvote'),
]
