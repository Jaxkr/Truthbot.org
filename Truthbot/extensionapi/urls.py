from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'getownerinfo/$', views.get_owner_info, name='getownerinfo'), #pass domain
]