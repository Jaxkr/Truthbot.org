from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def post_list(request):
    sort = request.GET.get('sort')
    if sort == 'hot':
        posts = Post.objects.all().order_by('-score')
    elif sort == 'new':
        posts = Post.objects.all().order_by('-timestamp')
    else:
        posts = Post.objects.all().order_by('-score')


    paginator = Paginator(posts, 40)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'news/news_list.html', {'posts': posts})

@login_required
def submit_post(request):
    form = SubmitLink()

    if request.method == 'POST':
        form = SubmitLink(request.POST)

        if form.is_valid():
            post = Post(title=form.cleaned_data['title'], link=form.cleaned_data['link'], author=request.user)
            post.save()

            return HttpResponseRedirect(reverse('postview', args=[post.slug]))

        else:
            return render(request, 'news/submit_post.html', {'form': form})

    return render(request, 'news/submit_post.html', {'form': form})

def post_view(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    comments = Comment.objects.filter(post=post)

    return render(request, 'news/post_view.html', {'post': post})







#voting ajax views
@login_required
def post_vote(request):
    if request.method == 'POST':
        post_id = request.POST.get('postid')
        post = Post.objects.get(pk=post_id)
        if PostVote.objects.filter(post=post, user=request.user).exists():
            p = PostVote.objects.get(post=post, user=request.user)
            p.delete()
            post.score -= 1
            post.save()
            return HttpResponse('removed')
        else:
            p = PostVote(post=post, user=request.user)
            p.save()
            post.score += 1
            post.save()
            return HttpResponse('added')
    else:
        return HttpResponse('')
