from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dash_index, name='dashboard'),
    url(r'^new-organization/$', views.organization_new, name='organizationnew')
]
