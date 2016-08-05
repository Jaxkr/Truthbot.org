from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .uniqueslug import unique_slugify

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User)
    link = models.CharField(max_length=2083, blank=False)
    title = models.CharField(max_length=350)
    timestamp = models.DateTimeField(auto_now=True)
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
    timestamp = models.DateTimeField(auto_now=True)



class PostVote(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)

class CommentVote(models.Model):
    pass
