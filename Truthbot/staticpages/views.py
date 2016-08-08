from django.shortcuts import render
from organizations.models import *
from contributors.models import *

# Create your views here.

def homepage(request):
    organization_count = Organization.objects.count()
    organization_domain_count = OrganizationDomain.objects.count()
    organization_wiki_count = OrganizationWiki.objects.count()

    top_contributors = Contributor.objects.all().order_by('-points')[:10]

    return render(request, 'staticpages/index.html', {'organization_count': organization_count, 'organization_domain_count': organization_domain_count, 'organization_wiki_count': organization_wiki_count, 'top_contributors': top_contributors})
