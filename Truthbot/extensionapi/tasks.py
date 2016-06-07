from celery import shared_task
from celery.utils.log import get_task_logger
from celery import task
import urllib.parse, json
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article

@shared_task
def create_organization(domain):
	base_wikipedia_url = 'https://en.wikipedia.org/w/api.php?'
	params = urllib.parse.urlencode({'action':'query','titles': domain, 'prop': 'revisions', 'rvprop': 'content', 'format': 'json', 'redirects': '1'})
	url = base_wikipedia_url + params
	response = urllib.request.urlopen(create_request(url))
	response_str = response.read().decode('utf-8')
	data = json.loads(response_str)
	page_title = data['query']['pages'][list(data['query']['pages'].keys())[0]]['title']
	params = urllib.parse.urlencode({'action':'parse','page': page_title, 'format': 'json'})
	url = base_wikipedia_url + params
	response = urllib.request.urlopen(create_request(url))
	response_str = response.read().decode('utf-8')
	data = json.loads(response_str)

	print(data)
	markup = data['parse']['text']['*']

	soup = BeautifulSoup(markup, 'html.parser')

	print(soup.prettify())


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