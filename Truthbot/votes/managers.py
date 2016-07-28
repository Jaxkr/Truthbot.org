from django.db import models
from django.db.models import Sum, Count
from .models import *
from articles.models import *
from organizations.models import *

class VoteManager(models.Manager):
    def cast_vote(self, obj, user, vote):
        if vote not in (+1, -1):
            raise ValueError('Invalid vote (must be +1/-1)')

        v = self.create(review=obj, user=user, vote=vote)

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

    def remove_vote(self, obj, user):
        pass
