from celery import shared_task
from .models import *
import time

@shared_task
def create_article(url):
	ArticleInProgress.objects.get(url=url).delete()
	print(url)