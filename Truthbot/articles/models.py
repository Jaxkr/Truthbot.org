from django.db import models

# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=300, blank=False)
	summary = models.CharField(max_length=1000, blank=False)
	url = models.CharField(max_length=2083, blank=False, unique=True)
	image_url = models.CharField(max_length=2083, blank=False)
	related_articles = models.ManyToManyField('Article', blank=True)
	keywords = models.CharField(max_length=5000)

	def __str__(self):
		return self.title