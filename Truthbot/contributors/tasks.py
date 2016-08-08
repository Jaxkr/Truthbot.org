from celery import shared_task
from .models import *
from news.models import *
from organizations.models import *
from django.db.models import Sum
from reversion.models import Revision
from django.contrib.auth.models import User

#honestly i just wanted to use celery for something
@shared_task
def compute_score(user):
    user = User.objects.get(pk=user)
    post_score_sum = Post.objects.filter(author=user).aggregate(Sum('score'))['score__sum'] or 0
    comment_score_sum = Comment.objects.filter(author=user).aggregate(Sum('score'))['score__sum'] or 0
    comment_replies_sum = CommentReply.objects.filter(author=user).count()
    wiki_edit_sum = OrganizationWiki.objects.filter(contributors=user).count() * 5
    reversion_sum = Revision.objects.filter(user=user).count()

    score = post_score_sum + comment_score_sum + comment_replies_sum + wiki_edit_sum + reversion_sum

    c = Contributor.objects.get(user=user)
    c.points = score
    c.save()
