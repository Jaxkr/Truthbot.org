from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pprint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
import json
import reversion
from reversion.models import Version

# Create your views here.

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
			with reversion.create_revision():
				org = Organization(name=form.cleaned_data['name'], url=form.cleaned_data['info_url'], description=form.cleaned_data['description'])
				org.save()
				reversion.set_user(request.user)

			return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))

		else:
			return render(request, 'organizations/organization_new.html', {'form': form})

	form = OrganizationForm()
	return render(request, 'organizations/organization_new.html', {'form': form})

@login_required
def organization_info(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	reviews = OrganizationReview.objects.filter(organization=org)

	return render(request, 'organizations/organization_info.html', {'org': org, 'reviews': reviews})

@login_required
def organization_create_review(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)

	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			with reversion.create_revision():
				new_review = OrganizationReview(tone=form.cleaned_data['tone'], text=form.cleaned_data['review'], organization=org, original_author=request.user)
				new_review.save()
				new_review.contributors.add(request.user)
				reversion.set_user(request.user)

			return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))
		else:
			return render(request, 'organizations/organization_review.html', {'form': form, 'org': org})
	form = ReviewForm()
	return render(request, 'organizations/organization_review.html', {'form' : form, 'org': org})


@login_required
def organization_review_view(request, review_pk):
	review = OrganizationReview.objects.get(pk=review_pk)
	versions = Version.objects.get_for_object(review)

	return render(request, 'organizations/organization_review_view.html', {'review' : review, 'versions': versions})

@login_required
def organization_review_confirm_rollback(request, edit_pk):
	version = Version.objects.get(pk=edit_pk)

	if request.method == 'POST':
		version.revert()
		return HttpResponseRedirect(reverse('organizationreviewview', args=[version.object_id]))

	return render(request, 'organizations/generic/confirm_rollback.html')


@login_required
def organization_edit_review(request, review_pk):
	review = OrganizationReview.objects.get(pk=review_pk)
	form = ReviewForm(initial={'review': review.text, 'tone': review.tone})

	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			if ((form.cleaned_data['review'] != review.text) or (form.cleaned_data['tone'] != review.tone)):
				with reversion.create_revision():
					review.text = form.cleaned_data['review']
					review.tone = form.cleaned_data['tone']
					review.contributors.add(request.user)
					review.save()
					reversion.set_user(request.user)

				return HttpResponseRedirect(reverse('organizationreviewview', args=[review.pk]))
		else:
			return render(request, 'organizations/organization_review.html', {'form': form, 'edit': True})

	return render(request, 'organizations/organization_review.html', {'form' : form, 'edit': True})

@login_required
def organization_modify_domains(request, organization_pk):# NOTMG OLD VERSION
	org = Organization.objects.get(pk=organization_pk)
	domains = OrganizationDomain.objects.filter(organization=org)
	deleted_domains = Version.objects.get_deleted(OrganizationDomain)

	if request.method == 'POST':
		form = AddDomain(request.POST)
		if form.is_valid():
			with reversion.create_revision():
				new_domain = OrganizationDomain(domain=form.cleaned_data['domain'], organization=org)
				new_domain.save()
				reversion.set_user(request.user)
			deleted_domains = Version.objects.get_deleted(OrganizationDomain)
		else:
			return render(request, 'organizations/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form})
	if 'domainrestoreid' in request.GET:
		version = Version.objects.get(pk=request.GET['domainrestoreid'])
		version.revert()
		return HttpResponseRedirect(reverse('organizationmodifydomains', args=[org.pk]))

	form = AddDomain()
	return render(request, 'organizations/organization_modify_domains.html', {'org': org, 'domains': domains, 'form': form, 'domain_removals': deleted_domains})


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

@login_required
def organization_modify(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	if request.method == 'POST':
		form = OrganizationForm(request.POST, request.FILES)
		if form.is_valid():
			#check if there are any changes
			if ((form.cleaned_data['name'] != org.name) or (form.cleaned_data['description'] != org.description) or (form.cleaned_data['info_url'] != org.url)):
				with reversion.create_revision():
					org.name = form.cleaned_data['name']
					org.description = form.cleaned_data['description']
					org.url = form.cleaned_data['info_url']
					org.save()
					reversion.set_user(request.user)
				return HttpResponseRedirect(reverse('organizationinfo', args=[org.pk]))
			else:
				return render(request, 'organizations/organization_modify.html', {'form': form, 'nochanges': True})
		else:
			return render(request, 'organizations/organization_modify.html', {'form': form})



	form = OrganizationForm(initial={'name': org.name, 'description': org.description, 'info_url': org.url})

	return render(request, 'organizations/organization_modify.html', {'form': form})

@login_required
def organization_edit_history(request, organization_pk):
	org = Organization.objects.get(pk=organization_pk)
	versions = Version.objects.get_for_object(org)

	# workaround to get the names of organizations in addition to their ID due to limitation in django-reversion
	for version in versions:
		version.named_child_organizations = []
		for child in version.field_dict['child_organizations']:
			child_organization = Organization.objects.get(pk=child)
			version.named_child_organizations.append((child_organization.name, child_organization.pk))
		print(version.named_child_organizations)


	return render(request, 'organizations/organization_edit_history.html', {'versions': versions, 'org': org})

def organization_confirm_rollback(request, edit_pk):
	version = Version.objects.get(pk=edit_pk)

	if request.method == 'POST':
		version.revert()
		return HttpResponseRedirect(reverse('organizationinfo', args=[version.object_id]))

	return render(request, 'organizations/generic/confirm_rollback.html')



@login_required
def organization_delete_domain(request, organization_pk):
	domain_pk = request.GET['domainid']
	domain = OrganizationDomain.objects.get(pk=domain_pk)
	org = domain.organization
	if request.method == 'POST':
		with reversion.create_revision():
			domain.delete()
		return HttpResponseRedirect(reverse('organizationmodifydomains', args=[domain.organization.pk]))
	return render(request, 'organizations/generic/confirm_remove_domain.html', {'domain': domain})

@login_required
def organization_remove_child(request, organization_pk):

	parent_organization = Organization.objects.get(pk=organization_pk)
	child_organization_pk = request.GET['childid']
	child_organization = Organization.objects.get(pk=child_organization_pk)

	if request.method == 'POST':
		with reversion.create_revision():
			parent_organization.child_organizations.remove(child_organization)
		return HttpResponseRedirect(reverse('organizationmodifychildren', args=[organization_pk]))
	

	return render(request, 'organizations/generic/confirm_remove_child.html', {'organization': parent_organization, 'childorg': child_organization})

@login_required
def organization_add_child(request, organization_parent_pk, organization_child_pk):

	child_organization = Organization.objects.get(pk=organization_child_pk)
	parent_organization = Organization.objects.get(pk=organization_parent_pk)

	if request.method == 'POST':
		with reversion.create_revision():
			parent_organization.child_organizations.add(child_organization)
		return HttpResponseRedirect(reverse('organizationmodifychildren', args=[organization_parent_pk]))

	return render(request, 'organizations/generic/confirm_add_child.html', {'organization': parent_organization, 'childorg': child_organization})
