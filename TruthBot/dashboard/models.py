from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.

class WebPage(models.Model):
	title = models.CharField(max_length=250, blank=False)
	url = models.CharField(max_length=2083, blank=False)

	def __str__(self):
		return self.title

class OrganizationDomain(models.Model):
	domain = models.CharField(max_length=200)
	organization = models.ForeignKey('Organization')

	def __str__(self):
		return self.domain

class Organization(models.Model):
	name = models.CharField(max_length=300, blank=False)
	description = models.CharField(max_length=1000, blank=False)
	logo = models.ImageField()
	url = models.CharField(max_length=2083, blank=False)
	child_organizations = models.ManyToManyField('Organization', blank=True)

	def __str__(self):
		return self.name



#logging actions for revision history

class LoggedOrganizationEdit(models.Model):
	organization_old_json = JSONField()
	user = models.ForeignKey(User)
	organization = models.ForeignKey('Organization')
	edit_time = models.DateTimeField(auto_now=True)


class LoggedOrganizationDomainRemoval(models.Model):
	domain_old_json = JSONField()
	organization = models.ForeignKey('Organization')
	user = models.ForeignKey(User)
	edit_time = models.DateTimeField(auto_now=True)

class LoggedOrganizationDomainAddition(models.Model):
	domain = models.ForeignKey('OrganizationDomain')
	organization = models.ForeignKey('Organization')
	user = models.ForeignKey(User)
	edit_time = models.DateTimeField(auto_now=True)