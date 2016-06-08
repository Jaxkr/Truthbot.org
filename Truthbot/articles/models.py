from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=300, blank=False)
	url = models.CharField(max_length=2083, blank=False, unique=True)
	related_articles = models.ManyToManyField('Article', blank=True)
	keywords = ArrayField(models.CharField(max_length=200), blank=True)
	date = models.DateTimeField(null=True)

	def __str__(self):
		return self.title