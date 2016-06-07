from django.shortcuts import render
from django.http import HttpResponse
import json
from urllib.parse import urlparse
from django.core import serializers
from pprint import pprint

from organizations.models import *
from extensionapi.tasks import create_organization


# Create your views here.


def get_page_info(request):
	requested_url = request.GET['url']
	requested_domain = urlparse(requested_url).netloc
	try:
		domain = OrganizationDomain.objects.get(domain=requested_domain)
		org = domain.organization
		org_dict = serializers.serialize("python", [org])
		parent_organizations = org.parent_organizations.all()
		parent_organizations_dict = serializers.serialize("python", parent_organizations)

		data_to_return_dict = {'organization': org_dict, 'parent_organizations': parent_organizations_dict}
		return api_response(data_to_return_dict)
	except OrganizationDomain.DoesNotExist:
		create_organization.delay(requested_domain)
		return api_response({'status': 'first'})




def api_response(data_dict):
	data_to_return = json.dumps(data_dict)
	response = HttpResponse(data_to_return, content_type='application/json')
	response['Access-Control-Allow-Origin'] = '*'
	return response