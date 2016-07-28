from django.db import models
from django.db.models import Sum, Count
from .models import *
from articles.models import *
from organizations.models import *

class VoteManager(models.Manager):
    def cast_vote(self, obj, user, vote):
        if vote not in (+1, -1):
            raise ValueError('Invalid vote (must be +1/-1)')

        if self.filter(review=obj, user=user).exists():
            v = self.get(review=obj, user=user)
            v.vote = vote
            v.save()
        else:
            v = self.create(review=obj, user=user, vote=vote)

    def remove_vote(self, obj, user):
        if self.filter(review=obj, user=user).exists():
            v = self.get(review=obj, user=user)
            v.delete()

    def get_user_vote(self, obj, user):
        if self.filter(review=obj, user=user).exists():
            v = self.get(review=obj, user=user)
            return v.vote
        else:
            return '0'

    def get_objects_voted_on(self, user):
        voted_on = self.filter(user=user)
        return voted_on

    def get_top_reviews(self, review_object):
        if type(review_object) == Article:
            model = ArticleReview
            results = self.filter(review__article = review_object).values('review_id').annotate(score=Sum('vote'))
        elif type(review_object) == Organization:
            model = OrganizationReview
            results = self.filter(review__organization = review_object).values('review_id').annotate(score=Sum('vote'))

        results.order_by('score')

        reviews = []
        for item in results:
            review = model.objects.get(pk=item['review_id'])
            reviews.append({'review': review, 'score': item['score']})

        return(reviews)
