from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'g/$', views.getCompanyFromWebpage, name='getCompanyFromWebpage'),
]