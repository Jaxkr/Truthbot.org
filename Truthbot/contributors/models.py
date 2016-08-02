from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contributor(models.Model):
    user = models.OneToOneField(User)
    points = models.IntegerField()
