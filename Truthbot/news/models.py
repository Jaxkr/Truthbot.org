from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .uniqueslug import unique_slugify
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User)
    link = models.CharField(max_length=2083, blank=False)
    title = models.CharField(max_length=350)
    timestamp = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self):
        slug_str = self.title
        unique_slugify(self, slug_str)
        super(Post, self).save()



class Comment(models.Model):
    post = models.ForeignKey('Post')
    author = models.ForeignKey(User)
    text = models.TextField()
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

#only a single level of reply
#reply comments are always ordered chronologically and cannot be voted on
class CommentReply(models.Model):
    post = models.ForeignKey('Post')
    comment = models.ForeignKey('Comment')
    author = models.ForeignKey(User)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['timestamp']


class PostVote(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)

class CommentVote(models.Model):
    comment = models.ForeignKey('Comment')
    user = models.ForeignKey(User)
