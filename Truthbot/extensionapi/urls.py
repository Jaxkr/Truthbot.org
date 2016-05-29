from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'getsiteinfo/$', views.get_site_info, name='getsiteinfo'), #pass domain
]