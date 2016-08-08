from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about/$', TemplateView.as_view(template_name="staticpages/about.html"), name='about'),
    url(r'^donate/$', TemplateView.as_view(template_name="staticpages/donate.html"), name='donate'),
    url(r'^reddit/$', TemplateView.as_view(template_name="staticpages/reddit.html"), name='reddit'),
]
