from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.dash_index, name='dashboard'),
    url(r'organizations/$', views.organization_root, name='organizationroot'),
    url(r'new-organization/$', views.organization_new, name='organizationnew'),
    url(r'organization/(?P<organization_pk>\d+)/$', views.organization_info, name='organizationinfo'),
    url(r'organization/(?P<organization_pk>\d+)/domains/$', views.organization_modify_domains, name='organizationmodifydomains'),
    url(r'organization-search/$', views.organization_search, name='organizationsearch'),
    url(r'organization/(?P<organization_pk>\d+)/edit-children/$', views.organization_modify_children, name='organizationmodifychildren'),



    #removal functions
    url(r'organization/(?P<organization_pk>\d+)/domains/remove/$', views.organization_delete_domain, name='organizationdeletedomain'),
    url(r'organization/(?P<organization_pk>\d+)/edit-children/remove/$', views.organization_remove_child, name='organizationremovechild'),
]
