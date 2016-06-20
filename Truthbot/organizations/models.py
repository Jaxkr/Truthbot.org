from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User

# Create your models here.
class OrganizationDomain(models.Model):
	domain = models.CharField(max_length=200, unique=True)
	organization = models.ForeignKey('Organization')

	def __str__(self):
		return self.domain

class Organization(models.Model):
	name = models.CharField(max_length=300, blank=False)
	description = models.CharField(max_length=1000, blank=False)
	url = models.CharField(max_length=2083, blank=False)
	child_organizations = models.ManyToManyField('Organization', blank=True, related_name='parent_organizations')
	wiki_url = models.CharField(max_length=2083, blank=False)

	def __str__(self):
		return self.name

class OrganizationComment(models.Model):
	POSITIVE_TONE = 'P'
	NEUTRAL_TONE = 'N'
	CRITICAL_TONE = 'C'

	COMMENT_TONE_CHOICES = (
		(POSITIVE_TONE, 'Positive'),
		(NEUTRAL_TONE, 'Neutral'),
		(CRITICAL_TONE, 'Critical')
		)

	tone = models.CharField(max_length=1, choices=COMMENT_TONE_CHOICES, default=NEUTRAL_TONE)
	text = models.CharField(max_length=300)

	
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