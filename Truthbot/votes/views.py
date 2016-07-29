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
        if request.GET['model'] == 'organizationreview':
            vote_type = int(request.GET['type'])
            review = OrganizationReview.objects.get(pk=request.GET['review'])
            OrganizationReviewVote.objects.cast_vote(review, request.user, vote_type)
        elif request.GET['model'] == 'articlereview':
            vote_type = int(request.GET['type'])
            review = ArticleReview.objects.get(pk=request.GET['review'])
            ArticleReviewVote.objects.cast_vote(review, request.user, vote_type)
        return HttpResponse('success')
