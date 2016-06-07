from celery import shared_task
from celery.utils.log import get_task_logger
from celery import task
import urllib.parse, json
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article
import newspaper
from articles.models import Article as ArticleModel


@shared_task
def create_organization(url):
	o = urllib.parse.urlsplit(url)
	url_without_path = o.scheme + '://' + o.netloc

	n = newspaper.build(url_without_path)
	n_brand = n.brand

	n_domains = []
	for category in n.category_urls():
		domain = urllib.parse.urlsplit(category).netloc
		if (domain not in n_domains):
			n_domains.append(domain)

	print(n_domains)

	



@shared_task
def parse_article(url):
	o = urllib.parse.urlsplit(url)

	if (len(o.path) > 1 and o.path != '/'): #avoid parsing home pages
		article = Article(url)
		article.download()
		article.parse()
		article.nlp()

		new_article = ArticleModel(title=article.title, summary=article.summary, url=url, image_url=article.top_image, keywords=', '.join(article.keywords))
		new_article.save()
	else:
		return

def create_request(url):
	return urllib.request.Request(
    	url, 
    	data=None, 
    	headers={
        'User-Agent': 'Truthbot Web Scraper/1.0 (https://github.com/Jaxkr/Truthbot.org; jacksonroberts25@gmail.com) urllib/Python3'
    	}
	)