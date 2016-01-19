from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dash_index(request):

	return render(request, 'dashboard/index.html')

@login_required
def organization_new(request):
	return render(request, 'dashboard/organization_new.html')