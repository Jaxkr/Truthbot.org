from django.db import models

# Create your models here.

class WebPage(models.Model):
	page_title = models.CharField(max_length=250, blank=False)
	page_url = models.CharField(max_length=2083, blank=False)

	def __unicode__(self):
		return self.page_title