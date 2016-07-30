from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from organizations.models import *
from articles.models import *

# Create your views here.
def cast_vote(request):
    if request.method != 'POST':
        return HttpResponse()
    elif request.method == 'POST':
        vote_type = int(request.GET['type'])
        if vote_type == 0:
            if request.GET['model'] == 'organizationreview':
                review = OrganizationReview.objects.get(pk=request.GET['review'])
                OrganizationReviewVote.objects.remove_vote(review, request.user)
            elif request.GET['model'] == 'articlereview':
                review = ArticleReview.objects.get(pk=request.GET['review'])
                ArticleReviewVote.objects.remove_vote(review, request.user)
            return HttpResponse('success')
        else:
            if request.GET['model'] == 'organizationreview':
                review = OrganizationReview.objects.get(pk=request.GET['review'])
                OrganizationReviewVote.objects.cast_vote(review, request.user, vote_type)
            elif request.GET['model'] == 'articlereview':
                review = ArticleReview.objects.get(pk=request.GET['review'])
                ArticleReviewVote.objects.cast_vote(review, request.user, vote_type)
                return HttpResponse('success')
