from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from organizations.models import *
from .tasks import create_article
import datetime
import math
from django.utils import timezone
from urllib.parse import urlparse
from .forms import *

# Create your views here.

def article_view(request, url):
	#this view is atrocious, but it seems efficient


	#get the parents of the requested article
	org = {}
	parents = {}
	org_exists = False
	have_article = False
	article = {}


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
		
	elif ArticleInProgress.objects.filter(url=url).exists():
		t1 = ArticleInProgress.objects.get(url=url).time_added
		now = datetime.datetime.now()
		elapsed = math.floor((now-t1).total_seconds())
	else:
		create_article.delay(url)
		a = ArticleInProgress(url=url)
		a.save()

	return render(request, 'articles/article.html', {'org': org, 'parents': parents, 'domain': requested_domain, 'org_exists': org_exists, 'article': article, 'have_article': have_article, 'seconds': elapsed})

def article_create_review(request, article_pk):
	article = Article.objects.get(pk=article_pk)

	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			new_review = ArticleReview(tone=form.cleaned_data['tone'], text=form.cleaned_data['review'], user=request.user, article=article)
			new_review.save()
			return HttpResponse('asdf')
		else:
			return render(request, 'article/article_review.html', {'form': form, 'org': org})

	form = ReviewForm()
	return render(request, 'articles/article_review.html', {'article': article, 'form': form})



