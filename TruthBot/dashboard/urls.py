from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dash_index, name='dashboard'),
    url(r'new-organization/$', views.organization_new, name='organizationnew'),
    url(r'organization/(?P<organization_pk>\d+)/$', views.organization_info, name='organizationinfo'),
    url(r'organization-domains/(?P<organization_pk>\d+)/$', views.organization_modify_domains, name='organizationdomains'),
]
