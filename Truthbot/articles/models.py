from django.db import models

# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=300, blank=False)
	summary = models.CharField(max_length=1000, blank=False)
	url = models.CharField(max_length=2083, blank=False)
	related_articles = models.ManyToManyField('Article', blank=True)

	def __str__(self):
		return self.name