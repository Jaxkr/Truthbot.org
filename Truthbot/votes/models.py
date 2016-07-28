from django.db import models
from django.contrib.auth.models import User
from articles.models import *
from organizations.models import *
from .managers import VoteManager


# Create your models here.

# GenericForeignKey is hellish, so a vote model has been created for every type of
# votable object. This is fine for now, as there are only two models

SCORES = (
    (+1, '+1'),
    (-1, '-1'),
)

class VotableObject(models.Model):
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField(choices=SCORES)
    time_stamp = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = (('user', 'review'))
        abstract = True


class ArticleReviewVote(VotableObject):
    review = models.ForeignKey(ArticleReview)


class OrganizationReviewVote(VotableObject):
    review = models.ForeignKey(OrganizationReview)