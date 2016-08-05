from django import template
from news.models import *

register = template.Library()

@register.simple_tag
def get_vote_color(obj, user, model):
    if model == 'post':
        if PostVote.objects.filter(post=obj, user=user).exists():
            return 'red'
        else:
            return 'black'
    elif model == 'comment':
        if CommentVote.objects.filter(comment=obj, user=user).exists():
            return 'red'
        else:
            return 'black'


@register.simple_tag
def get_has_voted(obj, user, model):
    if model == 'post':
        if PostVote.objects.filter(post=obj, user=user).exists():
            return 'yes'
        else:
            return 'no'
    elif model == 'comment':
        if CommentVote.objects.filter(comment=obj, user=user).exists():
            return 'yes'
        else:
            return 'no'
