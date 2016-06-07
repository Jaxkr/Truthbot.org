from celery import shared_task
from celery.utils.log import get_task_logger
from celery import task
import urllib.parse, json
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article

@shared_task
def create_organization(domain):
	pass


@shared_task
def get_article_info(url):
	pass




def create_request(url):
	return urllib.request.Request(
    	url, 
    	data=None, 
    	headers={
        'User-Agent': 'Truthbot Web Scraper/1.0 (https://github.com/Jaxkr/Truthbot.org; jacksonroberts25@gmail.com) urllib/Python3'
    	}
	)