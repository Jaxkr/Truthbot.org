from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'profile/(?P<user_pk>\d+)/$', views.view_profile, name='profile'),
]
