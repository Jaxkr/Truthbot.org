from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User)
    link = models.CharField(max_length=2083, blank=False)
    title = models.CharField(max_length=90)
    timestamp = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    author = models.ForeignKey(User)
    text = models.TextField()
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)



class PostVote(models.Model):
    pass

class CommentVote(models.Model):
    pass
