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
    wiki_url = models.CharField(max_length=2083, blank=False)

    def __str__(self):
        return self.name

@reversion.register()
class OrganizationReview(models.Model):
    POSITIVE_TONE = 'P'
    NEUTRAL_TONE = 'N'
    CRITICAL_TONE = 'C'

    REVIEW_TONE_CHOICES = (
        (POSITIVE_TONE, 'Positive'),
        (NEUTRAL_TONE, 'Neutral'),
        (CRITICAL_TONE, 'Critical')
        )

    tone = models.CharField(max_length=1, choices=REVIEW_TONE_CHOICES, default=NEUTRAL_TONE)
    text = models.CharField(max_length=3000)
    organization = models.ForeignKey('Organization')
    original_author = models.ForeignKey(User, related_name='original_author_of')
    contributors = models.ManyToManyField(User)
    points = models.IntegerField(default=1)
    time_created = models.DateTimeField(auto_now_add=True)
