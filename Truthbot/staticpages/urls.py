from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="staticpages/index.html"), name='homepage'),
    url(r'^about/$', TemplateView.as_view(template_name="staticpages/about.html"), name='about'),
]
