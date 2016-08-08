from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from news.models import *
from organizations.models import *
from .tasks import compute_score

# Create your views here.

def view_profile(request, user_pk):
    u = User.objects.get(pk=user_pk)

    if Contributor.objects.filter(user=u).exists():
        c = Contributor.objects.get(user=u)
    else:
        c = Contributor(user=u, points=0)
        c.save()

    recent_posts = Post.objects.filter(author=u)[:10]
    recent_wiki_edits = OrganizationWiki.objects.filter(contributors=u)[:10]

    compute_score.delay(u.pk)



    return render(request, 'contributors/profile_page.html', {'user': u, 'contributor': c, 'posts': recent_posts, 'recent_wiki_edits': recent_wiki_edits})
