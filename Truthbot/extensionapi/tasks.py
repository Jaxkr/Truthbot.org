from celery import shared_task
from celery.utils.log import get_task_logger
from celery import task
import urllib.parse, json
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article
import newspaper
from organizations.models import *
from articles.models import Article as ArticleModel

base_wikipedia_url = 'http://en.wikipedia.org/wiki/'
@shared_task
def create_organization(url): #this assumes that this organization doesn't exist, but makes NO assumptions about the existence of the parent organizations
	o = urllib.parse.urlsplit(url)
	url_without_path = o.scheme + '://' + o.netloc

	n = newspaper.build(url_without_path)
	n_brand = n.brand
	
	n_domains = []
	for category in n.category_urls():
		domain = urllib.parse.urlsplit(category).netloc
		if (domain not in n_domains):
			n_domains.append(domain)
	
	url = urllib.parse.urljoin(base_wikipedia_url, n_brand)
	response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
	soup = BeautifulSoup(response, 'html.parser')
	[s.extract() for s in soup('sup')]
	intro = soup.find('p').getText()
	infobox_table = soup.find('table', { "class" : "infobox" })
	org_name = soup.find('h1', { "class" : "firstHeading" }).text
	infobox_rows = infobox_table.find_all('tr')
	infobox_data = {}
	for row in infobox_rows:
		if row.find('th'):
			key = row.find('th').text
			value = row.find('td')
			infobox_data[key.replace('\xa0', ' ')] =  value
	web_address = ''
	if ('Web address' in infobox_data):
		web_address = infobox_data['Web address'].find('a')['href']
	elif ('Website' in infobox_data):
		web_address = infobox_data['Website'].find('a')['href']

	if not Organization.objects.filter(name=org_name).exists():
		org = Organization(name=org_name, description=intro, url=web_address)
		org.save()
	else:
		return

	#and now create and link domains...
	for domain in n_domains:
		d = OrganizationDomain(domain=domain, organization=org)
		d.save()

	if ('Owner' in infobox_data):
		owner = {}

		#if there are any links in the infobox...
		if (infobox_data['Owner'].find('a')):
			#simply get the last link for now
			link = infobox_data['Owner'].find_all('a')[-1]
			owner['name'] = link.text
			owner['wikilink'] = link['href']
		else:
			#or just get the name
			owner['name'] = infobox_data['Owner'].text

		# and find any owners
		recursive_create_parent(owner, org)
	elif ('Parent' in infobox_data):
		owner = {}

		#if there are any links in the infobox...
		if (infobox_data['Parent'].find('a')):
			#simply get the last link for now
			link = infobox_data['Parent'].find_all('a')[-1]
			owner['name'] = link.text
			owner['wikilink'] = link['href']
		else:
			#or just get the name
			owner['name'] = infobox_data['Parent'].text

		# and find any owners
		recursive_create_parent(owner, org)
	elif ('Owned by' in infobox_data):
		owner = {}

		#if there are any links in the infobox...
		if (infobox_data['Owned by'].find('a')):
			#simply get the last link for now
			link = infobox_data['Owned by'].find_all('a')[-1]
			owner['name'] = link.text
			owner['wikilink'] = link['href']
		else:
			#or just get the name
			owner['name'] = infobox_data['Owned by'].text

		# and find any owners
		recursive_create_parent(owner, org)
	elif ('Owner(s)' in infobox_data):
		owner = {}

		#if there are any links in the infobox...
		if (infobox_data['Owner(s)'].find('a')):
			#simply get the last link for now
			link = infobox_data['Owner(s)'].find_all('a')[-1]
			owner['name'] = link.text
			owner['wikilink'] = link['href']
		else:
			#or just get the name
			owner['name'] = infobox_data['Owner(s)'].text

		# and find any owners
		recursive_create_parent(owner, org)







@shared_task
def parse_article(url):
	'''
	o = urllib.parse.urlsplit(url)

	if (len(o.path) > 1 and o.path != '/'): #avoid parsing home pages
		article = Article(url)
		article.download()
		article.parse()
		article.nlp()

		new_article = ArticleModel(title=article.title, url=url)
		new_article.save()
	else:
		return
	'''
	pass

def recursive_create_parent(owner_obj, child_organization):
	if ('wikilink' in owner_obj):
		#really should DRY this up
		url = urllib.parse.urljoin(base_wikipedia_url, owner_obj['wikilink'])
		response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
		soup = BeautifulSoup(response, 'html.parser')
		[s.extract() for s in soup('sup')]
		intro = soup.find('p').getText()
		infobox_table = soup.find('table', { "class" : "infobox" })
		org_name = soup.find('h1', { "class" : "firstHeading" }).text
		infobox_rows = infobox_table.find_all('tr')
		infobox_data = {}
		for row in infobox_rows:
			if row.find('th'):
				key = row.find('th').text
				value = row.find('td')
				infobox_data[key.replace('\xa0', ' ')] =  value
		web_address = ''
		if ('Web address' in infobox_data):
			web_address = infobox_data['Web address'].find('a')['href']
		elif ('Website' in infobox_data):
			web_address = infobox_data['Website'].find('a')['href']

		if not Organization.objects.filter(name=org_name).exists():
			new_organization = Organization(name=org_name, description=intro, url=web_address)
			new_organization.save()
			new_organization.child_organizations.add(child_organization)
			new_organization.save()
		else:
			new_organization = Organization.objects.get(name=org_name)
			new_organization.save()
			new_organization.child_organizations.add(child_organization)
			new_organization.save()

		if ('Owner' in infobox_data):
			owner = {}

			#if there are any links in the infobox...
			if (infobox_data['Owner'].find('a')):
				#simply get the last link for now
				link = infobox_data['Owner'].find_all('a')[-1]
				owner['name'] = link.text
				owner['wikilink'] = link['href']
			else:
				#or just get the name
				owner['name'] = infobox_data['Owner'].text

			# and find any owners
			recursive_create_parent(owner, new_organization)
		elif ('Parent' in infobox_data):
			owner = {}

			#if there are any links in the infobox...
			if (infobox_data['Parent'].find('a')):
				#simply get the last link for now
				link = infobox_data['Parent'].find_all('a')[-1]
				owner['name'] = link.text
				owner['wikilink'] = link['href']
			else:
				#or just get the name
				owner['name'] = infobox_data['Parent'].text

			# and find any owners
			recursive_create_parent(owner, new_organization)
		elif ('Owned by' in infobox_data):
			owner = {}

			#if there are any links in the infobox...
			if (infobox_data['Owned by'].find('a')):
				#simply get the last link for now
				link = infobox_data['Owned by'].find_all('a')[-1]
				owner['name'] = link.text
				owner['wikilink'] = link['href']
			else:
				#or just get the name
				owner['name'] = infobox_data['Owned by'].text

			# and find any owners
			recursive_create_parent(owner, new_organization)
		elif ('Owner(s)' in infobox_data):
			owner = {}

			#if there are any links in the infobox...
			if (infobox_data['Owner(s)'].find('a')):
				#simply get the last link for now
				link = infobox_data['Owner(s)'].find_all('a')[-1]
				owner['name'] = link.text
				owner['wikilink'] = link['href']
			else:
				#or just get the name
				owner['name'] = infobox_data['Owner(s)'].text

			# and find any owners
			recursive_create_parent(owner, new_organization)


		
	else:
		#we just got a name and no article so we can't really do much
		new_organization = Organization(name=owner_obj['name'])
		new_organization.save()
		new_organization.child_organizations.add(child_organization)
		new_organization.save()

def create_request(url):
	return urllib.request.Request(
    	url, 
    	data=None, 
    	headers={
        'User-Agent': 'Truthbot Web Scraper/1.0 (https://github.com/Jaxkr/Truthbot.org; jacksonroberts25@gmail.com) urllib/Python3'
    	}
	)

