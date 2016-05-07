from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pprint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import DeleteView


# Create your views here.

@login_required
def dash_index(request):
	return render(request, 'dashboard/index.html')

@login_required
def organization_search(request):
	search_form = OrganizationSearch(request.GET)
	search_term = search_form.data['search_term']

	#now that's what i call a search engine
	organizations = Organization.objects.filter(name__istartswith=search_term)


	return render(request, 'dashboard/organization_search.html', {'form': search_form, 'term': search_term, 'organizations': organizations})

@login_required
def organization_root(request):  
	organizations_list = Organization.objects.all()
	paginator = Paginator(organizations_list, 25)
	page = request.GET.get('page')
	search_form = OrganizationSearch()

	try:
		organizations = paginator.page(page)
	except PageNotAnInteger:
		organizations = paginator.page(1)
	except EmptyPage:
		organizations = paginator.page(paginator.num_pages)

	return render(request, 'dashboard/organization_root.html', {'organizations': organizations, 'form': search_form})


@login_required
def organization_new(request):
	if request.method == 'POST':
		form = NewOrganization(request.POST, request.FILES)
		
		if form.is_valid():
			org = Organization(name=form.cleaned_data['name'], url=form.cleaned_data['info_url'], logo=form.cleaned_data['logo'], description=form.cleaned_data['description'])
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

@login_required
def organization_modify_domains(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	domains = OrganizationDomain.objects.filter(organization=org)

	if request.method == 'POST':
		form = AddDomain(request.POST)
		if form.is_valid():
			new_domain = OrganizationDomain(domain=form.cleaned_data['domain'], organization=org)
			new_domain.save()
		else:
			return render(request, 'dashboard/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form})


	form = AddDomain()
	return render(request, 'dashboard/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form})

@login_required
def organization_modify_children(request, organization_pk):
	search_form = OrganizationSearch()

	organization = Organization.objects.get(pk=organization_pk)
	organization_children = organization.child_organizations.all()

	search_form = OrganizationSearch(request.GET)
	if 'search_term' in search_form.data:
		search_term = search_form.data['search_term']
		organization_search_results = Organization.objects.filter(name__istartswith=search_term)



	return render(request, 'dashboard/organization_modify_children.html', {'form': search_form, 'organization': organization, 'organization_children': organization_children, 'organization_search_results': organization_search_results})


'''why am I not using class-based views for this? Because I don't really understand them or how they interact with decorators
and permissions and I don't really want to take the time to figure it out
so let it be known... TODO: reimplement these functions with class based or generic views if it would be better'''

@login_required
def organization_delete_domain(request, organization_pk):
	domain_pk = request.GET['domainid']
	domain = OrganizationDomain.objects.get(pk=domain_pk)
	if request.method == 'POST':
		domain.delete()
		return HttpResponseRedirect(reverse('organizationmodifydomains', args=[domain.organization.pk]))
	return render(request, 'dashboard/generic/confirm_remove_domain.html', {'domain': domain})

@login_required
def organization_remove_child(request, organization_pk):

	parent_organization = Organization.objects.get(pk=organization_pk)
	child_organization_pk = request.GET['childid']
	child_organization = Organization.objects.get(pk=child_organization_pk)

	if request.method == 'POST':
		parent_organization.child_organizations.remove(child_organization)
		return HttpResponseRedirect(reverse('organizationmodifychildren', args=[organization_pk]))
	

	return render(request, 'dashboard/generic/confirm_remove_child.html', {'organization': parent_organization, 'childorg': child_organization})

