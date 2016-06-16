from django.shortcuts import render
from .models import *
# Create your views here.

def alerts_home(request):
	alerts = AlertPosts.objects.all()
	return render(request, 'alerts/alerts_homepage.html', {'alerts': alerts})