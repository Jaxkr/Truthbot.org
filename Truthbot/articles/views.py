from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .tasks import create_article
import datetime
import math
from django.utils import timezone

# Create your views here.

def article_view(request, url):
	if Article.objects.filter(url=url).exists():
		return HttpResponse(url)
	elif ArticleInProgress.objects.filter(url=url).exists():
		t1 = ArticleInProgress.objects.get(url=url).time_added
		now = datetime.datetime.now()
		elapsed = math.floor((now-t1).total_seconds())
		return render(request, 'articles/article_progress.html', {'url': url, 'seconds': elapsed})
	else:
		create_article.delay(url)
		a = ArticleInProgress(url=url)
		a.save()
		return render(request, 'articles/article_progress.html', {'url': url, 'new': True})