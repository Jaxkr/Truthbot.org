from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'getownerinfo/$', views.get_owner_info, name='getownerinfo'), #pass url
	url(r'getarticleinfo/$', views.get_article_info, name='getarticleinfo') #pass url
]