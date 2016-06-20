from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.organization_root, name='organizationroot'),
    url(r'new-organization/$', views.organization_new, name='organizationnew'),
    url(r'organization/(?P<organization_pk>\d+)/$', views.organization_info, name='organizationinfo'),
    url(r'organization/(?P<organization_pk>\d+)/domains/$', views.organization_modify_domains, name='organizationmodifydomains'),
    url(r'organization-search/$', views.organization_search, name='organizationsearch'),
    url(r'organization/(?P<organization_pk>\d+)/edit-children/$', views.organization_modify_children, name='organizationmodifychildren'),
    url(r'organization/(?P<organization_pk>\d+)/edit/$', views.organization_modify, name='organizationmodify'),
    url(r'organization/(?P<organization_pk>\d+)/edit-history/$', views.organization_edit_history, name='organizationedithistory'),
    url(r'organization/(?P<organization_pk>\d+)/new-comment/$', views.organization_create_comment, name='organizationcreatecomment'),

    #confirmation functions
    url(r'organization/(?P<organization_pk>\d+)/domains/remove/$', views.organization_delete_domain, name='organizationdeletedomain'),
    url(r'organization/(?P<organization_pk>\d+)/edit-children/remove/$', views.organization_remove_child, name='organizationremovechild'),
    url(r'organization/(?P<organization_parent_pk>\d+)/edit-children/add/(?P<organization_child_pk>\d+)$', views.organization_add_child, name='organizationaddchild'),
    url(r'organization/edit-history/rollback/(?P<edit_pk>\d+)$', views.organization_confirm_rollback, name='organizationconfirmrollback'),
]
