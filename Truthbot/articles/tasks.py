from celery import shared_task
from .models import *
import time
import newspaper
import re
import tldextract
from bs4 import BeautifulSoup
import urllib.request

base_wikipedia_url = 'http://en.wikipedia.org/wiki/'

@shared_task
def create_article(url):
	ArticleInProgress.objects.get(url=url).delete()
	get_organization_info(url)

def get_organization_info(url, **kwargs):
	try:
		o = urllib.parse.urlsplit(url)
		url_without_path = o.scheme + '://' + o.netloc
		n = newspaper.build(url_without_path)
		n_domains = []
		for category in n.category_urls():
			domain = urllib.parse.urlsplit(category).netloc
			if (domain not in n_domains):
				n_domains.append(domain)
	except:
		return

	try:
		extracted = tldextract.extract(url_without_path)
		tld = "{}.{}".format(extracted.domain, extracted.suffix)
		url = urllib.parse.urljoin(base_wikipedia_url, tld)
		response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
		soup = BeautifulSoup(response, 'html.parser')
	except:
		pass
	try:
		url = urllib.parse.urljoin(base_wikipedia_url, n.brand)
		response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
		soup = BeautifulSoup(response, 'html.parser')
	except:
		return

	[s.extract() for s in soup('sup')]
	intro = soup.find('p').getText()
	infobox_table = soup.findAll('table', { "class" : "infobox" })
	if (infobox_table):
		infobox_table = infobox_table[0]
		infobox_data = parse_wikipedia_table(infobox_table)
		print(infobox_data)



def parse_wikipedia_table(infobox_table):
	infobox_rows = infobox_table.find_all('tr')
	infobox_data = {}
	for row in infobox_rows:
		if row.find('th'):
			key = row.find('th').text
			value = row.find('td')
			infobox_data[key.replace('\xa0', ' ')] =  value
	return infobox_data

def create_request(url):
	return urllib.request.Request(
    	url, 
    	data=None, 
    	headers={
        'User-Agent': 'Truthbot Web Scraper/1.0 (https://github.com/Jaxkr/Truthbot.org; jacksonroberts25@gmail.com) urllib/Python3'
    	}
	)