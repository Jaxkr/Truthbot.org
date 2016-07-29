from django.shortcuts import render
from urllib.parse import urlparse
from organizations.models import *
from articles.models import *
from articles.tasks import create_article
import datetime
import math
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Create your views here.

def article(request, url):
    #this view is atrocious, but it seems efficient

    #get the parents of the requested article
    org = {}
    parents = {}
    org_exists = False
    have_article = False
    article = {}
    have_article_reviews = False
    sorting = request.GET['sorting'] if ('sorting' in request.GET) else 'top'
    article_reviews = {}

    url_validator = URLValidator()

    try:
        url_validator(url)
    except ValidationError:
        return HttpResponse('Invalid url')


    requested_domain = urlparse(url).netloc
    if (OrganizationDomain.objects.filter(domain=requested_domain).exists()):
        organization_domain = OrganizationDomain.objects.get(domain=requested_domain)

        org = organization_domain.organization
        parents = []
        org_parents = org.parent_organizations.all()
        if len(org_parents) > 0:
            hasParents = True
        else:
            hasParents = False
        current_org = org
        while hasParents:
            parent = current_org.parent_organizations.all()[0]
            parents.append(parent)
            if len(parent.parent_organizations.all()) > 0:
                current_org = parent
            else:
                hasParents = False
        org_exists = True
        # to return: org, parents, org_exists

    elapsed = 0

    if Article.objects.filter(url=url).exists():
        article = Article.objects.get(url=url)
        have_article = True

        if ArticleReview.objects.filter(article=article).exists():
            have_article_reviews = True
            if request.GET.get('sort') == 'new':
                reviews = ArticleReview.objects.filter(article=article).order_by('-time_created')
                reviews_list = []
                for review in reviews:
                    reviews_list.append({'review': review, 'score': ArticleReviewVote.objects.get_score(review)['score']})
                article_reviews = reviews_list
            else:
                article_reviews = ArticleReviewVote.objects.get_top_reviews(review_object=article)

    elif PageInProgress.objects.filter(url=url).exists():
        t1 = PageInProgress.objects.get(url=url).time_added
        now = datetime.datetime.now()
        elapsed = math.floor((now-t1).total_seconds())
    else:
        create_article.delay(url)
        a = PageInProgress(url=url)
        a.save()


    return render(request, 'public/article.html', {'org': org, 'parents': parents,
                                                    'domain': requested_domain, 'org_exists': org_exists,
                                                    'article': article, 'have_article': have_article,
                                                    'seconds': elapsed, 'have_article_reviews': have_article_reviews,
                                                    'article_reviews': article_reviews})
