from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'getpageinfo/$', views.get_page_info, name='getsiteinfo'), #pass domain
]