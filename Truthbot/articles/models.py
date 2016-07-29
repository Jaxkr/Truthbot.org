from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
import reversion

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=300, blank=False)
    url = models.CharField(max_length=2083, blank=False, unique=True)
    time_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

@reversion.register() # only this as it's the only model that isn't auto-generated
class ArticleReview(models.Model):
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
    article = models.ForeignKey('Article')
    original_author = models.ForeignKey(User, related_name='article_original_author_of')
    contributors = models.ManyToManyField(User)
    time_created = models.DateTimeField(auto_now_add=True)


class PageInProgress(models.Model):
    url = models.CharField(max_length=2083, blank=False, unique=True)
    time_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
