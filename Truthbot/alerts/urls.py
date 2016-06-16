from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.alerts_home, name='alerts')
]