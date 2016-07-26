from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# Create your models here.

class Vote(models.Model):
	VOTE_CHOICES = (('up', 1), ('down', -1))

	user = models.ForeignKey(User)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()
	vote_type = models.IntegerField(choices=VOTE_CHOICES)