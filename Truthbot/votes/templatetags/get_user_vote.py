from django import template
from votes.models import *

register = template.Library()

@register.simple_tag
def get_vote_color(obj, user):
    color = 'black'

    if OrganizationReviewVote.objects.get_user_vote(obj, user) == 1:
        color = 'red'
    elif OrganizationReviewVote.objects.get_user_vote(obj, user) == -1:
        color = 'blue'

    return color
