from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
import hashlib

# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=300, blank=False)
	url = models.CharField(max_length=2083, blank=False, unique=True)
	related_articles = models.ManyToManyField('Article', blank=True)

	def __str__(self):
		return self.title

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
	user = models.ForeignKey(User)

class ArticleInProgress(models.Model):
	url = models.CharField(max_length=2083, blank=False, unique=True)
	time_added = models.DateTimeField(auto_now=True)

class LoggedArticleReviewEdit(models.Model):
	review_old_json = JSONField()
	user = models.ForeignKey(User)
	review = models.ForeignKey('ArticleReview')
	edit_time = models.DateTimeField(auto_now=True)
	edit_hash = models.CharField(max_length=20, unique=True)

	def save(self, **kwargs):
		self.edit_hash = hashlib.sha256((str(self.review_old_json) + str(self.review.pk)).encode('utf-8')).hexdigest()[:20]
		super().save(**kwargs)