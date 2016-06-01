from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pprint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
import json

# Create your views here.

@login_required
def dash_index(request):
	return render(request, 'organizations/index.html')

@login_required
def organization_search(request):
	search_form = OrganizationSearch(request.GET)
	search_term = search_form.data['search_term']

	#now that's what i call a search engine
	organizations = Organization.objects.filter(name__istartswith=search_term)


	return render(request, 'organizations/organization_search.html', {'form': search_form, 'term': search_term, 'organizations': organizations})

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

	return render(request, 'organizations/organization_root.html', {'organizations': organizations, 'form': search_form})


@login_required
def organization_new(request):
	if request.method == 'POST':
		form = OrganizationForm(request.POST, request.FILES)
		
		if form.is_valid():
			org = Organization(name=form.cleaned_data['name'], url=form.cleaned_data['info_url'], logo=form.cleaned_data['logo'], description=form.cleaned_data['description'])
			org.save()
			return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))

		else:
			return render(request, 'organizations/organization_new.html', {'form': form})

	form = OrganizationForm()
	return render(request, 'organizations/organization_new.html', {'form': form})

@login_required
def organization_info(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)

	return render(request, 'organizations/organization_info.html', {'org': org})

@login_required
def organization_modify_domains(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	domains = OrganizationDomain.objects.filter(organization=org)

	if request.method == 'POST':
		form = AddDomain(request.POST)
		if form.is_valid():
			new_domain = OrganizationDomain(domain=form.cleaned_data['domain'], organization=org)
			new_domain.save()
			logged_domain_addition = LoggedOrganizationDomainAddition(domain=new_domain, organization=org, user=request.user)
			logged_domain_addition.save()
		else:
			return render(request, 'organizations/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form})


	form = AddDomain()
	return render(request, 'organizations/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form})

@login_required
def organization_modify_children(request, organization_pk):
	search_form = OrganizationSearch()

	organization = Organization.objects.get(pk=organization_pk)
	organization_children = organization.child_organizations.all()

	search_form = OrganizationSearch(request.GET)
	if 'search_term' in search_form.data:
		search_term = search_form.data['search_term']
		organization_search_results = Organization.objects.filter(name__istartswith=search_term)
		return render(request, 'organizations/organization_modify_children.html', {'form': search_form, 'organization': organization, 'organization_children': organization_children, 'organization_search_results': organization_search_results})



	return render(request, 'organizations/organization_modify_children.html', {'form': search_form, 'organization': organization, 'organization_children': organization_children})

def organization_modify(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	if request.method == 'POST':
		form = OrganizationEditForm(request.POST, request.FILES)
		if form.is_valid():
			#check if there are any changes
			if ((form.cleaned_data['name'] != org.name) or (form.cleaned_data['description'] != org.description) or (form.cleaned_data['info_url'] != org.url)):
				serialized_data = serializers.serialize("json", [org])
				organization_old = LoggedOrganizationEdit(organization_old_json=serialized_data, organization=org, user=request.user)
				organization_old.save()

				org.name = form.cleaned_data['name']
				org.description = form.cleaned_data['description']
				org.url = form.cleaned_data['info_url']
				org.save()
				return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))
			else:
				return render(request, 'organizations/organization_modify.html', {'form': form, 'nochanges': True})
		else:
			return render(request, 'organizations/organization_modify.html', {'form': form})



	form = OrganizationEditForm(initial={'name': org.name, 'logo': org.logo, 'description': org.description, 'info_url': org.url})

	return render(request, 'organizations/organization_modify.html', {'form': form})

@login_required
def organization_edit_history(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	logged_edits = LoggedOrganizationEdit.objects.filter(organization=org)[:20]
	logged_edit_objects = []

	for edit in logged_edits:
		logged_edit_objects.append({'old_object': json.loads(edit.organization_old_json)[0]['fields'], 'edit': edit})


	return render(request, 'organizations/organization_edit_history.html', {'logged_edits': logged_edit_objects, 'org': org})

def organization_confirm_rollback(request, edit_pk):
	pass


def webpage_view(request, webpage_id):
	pass

@login_required
def organization_delete_domain(request, organization_pk):
	domain_pk = request.GET['domainid']
	domain = OrganizationDomain.objects.get(pk=domain_pk)
	org = domain.organization
	if request.method == 'POST':
		serialized_data = serializers.serialize("json", [domain])
		logged_domain_deletion = LoggedOrganizationDomainRemoval(domain_old_json=serialized_data, organization=org, user=request.user)
		logged_domain_deletion.save()
		domain.delete()
		return HttpResponseRedirect(reverse('organizationmodifydomains', args=[domain.organization.pk]))
	return render(request, 'organizations/generic/confirm_remove_domain.html', {'domain': domain})

@login_required
def organization_remove_child(request, organization_pk):

	parent_organization = Organization.objects.get(pk=organization_pk)
	child_organization_pk = request.GET['childid']
	child_organization = Organization.objects.get(pk=child_organization_pk)

	if request.method == 'POST':
		serialized_data = serializers.serialize("json", [parent_organization])
		organization_old = LoggedOrganizationEdit(organization_old_json=serialized_data, organization=parent_organization, user=request.user)
		organization_old.save()
		parent_organization.child_organizations.remove(child_organization)
		return HttpResponseRedirect(reverse('organizationmodifychildren', args=[organization_pk]))
	

	return render(request, 'organizations/generic/confirm_remove_child.html', {'organization': parent_organization, 'childorg': child_organization})

@login_required
def organization_add_child(request, organization_parent_pk, organization_child_pk):

	child_organization = Organization.objects.get(pk=organization_child_pk)
	parent_organization = Organization.objects.get(pk=organization_parent_pk)

	if request.method == 'POST':
		serialized_data = serializers.serialize("json", [parent_organization])
		organization_old = LoggedOrganizationEdit(organization_old_json=serialized_data, organization=parent_organization, user=request.user)
		organization_old.save()
		parent_organization.child_organizations.add(child_organization)
		return HttpResponseRedirect(reverse('organizationmodifychildren', args=[organization_parent_pk]))

	return render(request, 'organizations/generic/confirm_add_child.html', {'organization': parent_organization, 'childorg': child_organization})


