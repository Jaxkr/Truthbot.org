from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pprint
from django.core.urlresolvers import reverse


# Create your views here.

@login_required
def dash_index(request):

	return render(request, 'dashboard/index.html')

@login_required
def organization_new(request):
	if request.method == 'POST':
		form = NewOrganization(request.POST, request.FILES)
		
		if form.is_valid():
			org = Organization(name=form.cleaned_data['name'], info_url=form.cleaned_data['info_url'], logo=form.cleaned_data['logo'])
			org.save()
			return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))

		else:
			return render(request, 'dashboard/organization_new.html', {'form': form})

	form = NewOrganization()
	return render(request, 'dashboard/organization_new.html', {'form': form})
	
@login_required
def organization_info(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)

	return render(request, 'dashboard/organization_info.html', {'org': org})