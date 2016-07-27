from django.db import models
 
class VoteManager(models.Manager):
    def cast_vote(self, obj, user, vote):
        if vote not in (+1, -1):
            raise ValueError('Invalid vote (must be +1/-1)')
 
        v = self.create(review=obj, user=user, vote=vote)

    def remove_vote(self, obj, user):
        pass