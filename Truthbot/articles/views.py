from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from organizations.models import *
from .tasks import *
import datetime
import math
from django.utils import timezone
from urllib.parse import urlparse
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse, reverse_lazy
import reversion
from reversion.models import Version
from votes.models import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.
def articles_index(request):
    articles_list = Article.objects.all().order_by('-time_created')
    paginator = Paginator(articles_list, 25)
    page = request.GET.get('page')
    form = GoToArticle()

    if request.method == 'POST':
        form = GoToArticle(request.POST)
        url = form.data['article_url']
        return HttpResponseRedirect(reverse('article', args=[url]))

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'articles/articles.html', {'articles': articles, 'form': form})

def article_view(request, url):
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
    else:
        get_organization_info.delay(url)

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
        get_article_info.delay(url)
        a = PageInProgress(url=url)
        a.save()



    return render(request, 'articles/article.html', {'org': org, 'parents': parents,
                                                    'domain': requested_domain, 'org_exists': org_exists,
                                                    'article': article, 'have_article': have_article,
                                                    'seconds': elapsed, 'have_article_reviews': have_article_reviews,
                                                    'article_reviews': article_reviews})

@login_required
def article_create_review(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            with reversion.create_revision():
                new_review = ArticleReview(tone=form.cleaned_data['tone'], text=form.cleaned_data['review'], original_author=request.user, article=article)
                new_review.save()
                new_review.contributors.add(request.user)
                reversion.set_user(request.user)
            ArticleReviewVote.objects.cast_vote(new_review, request.user, +1)
            return HttpResponseRedirect(reverse('articlereviewview', args=[new_review.pk]))
        else:
            return render(request, 'article/article_review.html', {'form': form, 'org': org})

    form = ReviewForm()
    return render(request, 'articles/article_review.html', {'article': article, 'form': form})

@login_required
def article_edit_review(request, review_pk):
    review = ArticleReview.objects.get(pk=review_pk)
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
                return HttpResponseRedirect(reverse('articlereviewview', args=[review.pk]))
        else:
            return render(request, 'articles/article_review.html', {'form': form, 'edit': True})

    return render(request, 'articles/article_review.html', {'form' : form, 'edit': True})

def article_review_view(request, review_pk):
    review = ArticleReview.objects.get(pk=review_pk)
    review_edits = Version.objects.get_for_object(review)
    score = ArticleReviewVote.objects.get_score(obj=review)
    return render(request, 'articles/article_review_view.html', {'review' : review, 'edits': review_edits, 'reviewscore': score})


@login_required
def article_review_confirm_rollback(request, edit_pk):
    version = Version.objects.get(pk=edit_pk)
    if request.method == 'POST':
        version.revert()
        return HttpResponseRedirect(reverse('articlereviewview', args=[version.object_id]))

    return render(request, 'organizations/generic/confirm_rollback.html')
