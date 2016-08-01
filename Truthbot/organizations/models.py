from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
import reversion

# Create your models here.
@reversion.register()
class OrganizationDomain(models.Model):
    domain = models.CharField(max_length=200, unique=True)
    organization = models.ForeignKey('Organization')

    def __str__(self):
        return self.domain

@reversion.register()
class Organization(models.Model):
    name = models.CharField(max_length=300, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    url = models.CharField(max_length=2083, blank=False)
    child_organizations = models.ManyToManyField('Organization', blank=True, related_name='parent_organizations')
    wiki = models.ForeignKey('OrganizationWiki')

    def __str__(self):
        return self.name

@reversion.register()
class OrganizationWiki(models.Model):
    text = models.TextField()
    contributors = models.ManyToManyField(User)
    time_created = models.DateTimeField(auto_now=True)
    time_last_edited = models.DateTimeField()
