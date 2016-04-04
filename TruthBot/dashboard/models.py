from django.db import models

# Create your models here.

class WebPage(models.Model):
	title = models.CharField(max_length=250, blank=False)
	url = models.CharField(max_length=2083, blank=False)

	def __str__(self):
		return self.title

class OrganizationHost(models.Model):
	url = models.CharField(max_length=200)

	def __str__(self):
		return self.url

class Organization(models.Model):
	name = models.CharField(max_length=300, blank=False)
	description = models.CharField(max_length=1000, blank=False)
	logo = models.ImageField()
	url = models.CharField(max_length=2083, blank=False)
	site_urls = models.ManyToManyField('OrganizationHost')
	child_organizations = models.ManyToManyField('Organization', blank=True)

	def __str__(self):
		return self.name