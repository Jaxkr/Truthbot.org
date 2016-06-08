from django.shortcuts import render
from django.http import HttpResponse
import json
from urllib.parse import urlparse
from django.core import serializers
from pprint import pprint

from organizations.models import *
from extensionapi.tasks import parse_article, create_organization
from articles.models import *


# Create your views here.


def get_owner_info(request):
	requested_url = request.GET['url']
	requested_domain = urlparse(requested_url).netloc
	try:
		domain = OrganizationDomain.objects.get(domain=requested_domain)
		org = domain.organization
		org_dict = serializers.serialize("python", [org])
		global parents
		parents = []
		recursive_get_parents(org)
		data_to_return_dict = {'status': 'success', 'organization': org_dict, 'domain': requested_domain, 'parents': parents}
		return api_response(data_to_return_dict)
	except OrganizationDomain.DoesNotExist:
		create_organization.delay(requested_url)
		return api_response({'status': 'notfound'})


def get_article_info(request):
	requested_url = request.GET['url']
	try:
		article = Article.objects.get(url=requested_url)
		article_dict = serializers.serialize("python", [article])
		article_dict = {'status': 'success', 'article': article_dict}
		return api_response(article_dict)
	except Article.DoesNotExist:
		parse_article.delay(requested_url)
		return api_response({'status': 'first'})



def api_response(data_dict):
	data_to_return = json.dumps(data_dict)
	response = HttpResponse(data_to_return, content_type='application/json')
	response['Access-Control-Allow-Origin'] = '*'
	return response

def recursive_get_parents(organization):
	global parents
	if organization.parent_organizations.all().count() > 0:
		org = organization.parent_organizations.all()[0]
		parents.append(serializers.serialize("python", [org]))
		recursive_get_parents(org)