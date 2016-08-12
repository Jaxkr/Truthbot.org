from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import urlparse
import json
from organizations.models import *
from django.core import serializers
from datetime import datetime, timedelta
from news.models import Post

# Create your views here.

def get_org_info(request):
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
        return api_response({'status': 'notfound'})


def get_posts(request):
    time_threshold = timezone.now() - timedelta(hours=20)
    posts = Post.objects.filter(timestamp__gt=time_threshold).order_by('-score')[:5]

    posts_list = []
    for post in posts:
        posts_list.append({'title': post.title, 'slug': post.slug, 'link': post.link, 'comment_count': post.comment_set.count() + post.commentreply_set.count()})

    return api_response(posts_list)




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
