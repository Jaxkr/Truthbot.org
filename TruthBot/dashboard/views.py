from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pprint

# Create your views here.

@login_required
def dash_index(request):

	return render(request, 'dashboard/index.html')

@login_required
def organization_new(request):
	if request.method == 'POST':
		form = NewOrganization(request.POST, request.FILES)
		
		if form.is_valid():
			org = Organization(name=form.cleaned_data['name'], info_url=form.cleaned_data['info_url'])
			org.save()
		else:
			return render(request, 'dashboard/organization_new.html', {'form': form})

	form = NewOrganization()
	return render(request, 'dashboard/organization_new.html', {'form': form})