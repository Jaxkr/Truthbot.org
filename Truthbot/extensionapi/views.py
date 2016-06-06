from django.shortcuts import render
from django.http import HttpResponse
import json
from urllib.parse import urlparse
from django.core import serializers
from pprint import pprint

from organizations.models import *
# Create your views here.


def get_site_info(request):
	requested_url = request.GET['url']
	requested_domain = urlparse(requested_url).netloc
	domain = OrganizationDomain.objects.get(domain=requested_domain)
	org = domain.organization
	org_dict = serializers.serialize("python", [org])
	parent_organizations = org.parent_organizations.all()
	parent_organizations_dict = serializers.serialize("python", parent_organizations)

	

	data_to_return_dict = {'organization': org_dict}
	data_to_return = json.dumps(data_to_return_dict)
	response = HttpResponse(data_to_return, content_type='application/json')
	response['Access-Control-Allow-Origin'] = '*'
	return response