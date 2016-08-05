from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


# Create your views here.

def post_list(request):
    sort = request.GET.get('sort')
    if sort == 'hot':
        time_threshold = timezone.now() - timedelta(hours=12)
        posts = Post.objects.filter(timestamp__gt=time_threshold).order_by('-score')
    elif sort == 'new':
        posts = Post.objects.all().order_by('-timestamp')
    else:
        time_threshold = timezone.now() - timedelta(hours=12)
        posts = Post.objects.filter(timestamp__gt=time_threshold).order_by('-score')


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
    sort = request.GET.get('sort')

    if sort == 'top':
        comments = Comment.objects.filter(post=post).order_by('-score')
    elif sort == 'new':
        comments = Comment.objects.filter(post=post).order_by('-timestamp')
    else:
        comments = Comment.objects.filter(post=post).order_by('-score')

    form = NewComment()

    if request.method == 'POST':
        form = NewComment(request.POST)

        if form.is_valid():
            comment = Comment(text=form.cleaned_data['text'], post=post, author=request.user)
            comment.save()

            return HttpResponseRedirect(reverse('postview', args=[post.slug]))

        else:
            return render(request, 'news/post_view.html', {'post': post, 'form': form, 'comments': comments})


    return render(request, 'news/post_view.html', {'post': post, 'form': form, 'comments': comments})

def comment_reply(request, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        form = NewComment(request.POST)

        if form.is_valid():
            r = CommentReply(post=comment.post, comment=comment, author=request.user, text=form.cleaned_data['text'])
            r.save()

            return HttpResponseRedirect(reverse('postview', args=[comment.post.slug]) + '#reply-'+str(r.pk))
    else:
        return HttpResponse('no')

def comment_perma(request, post_slug, comment_pk):
    post = Post.objects.get(slug=post_slug)
    comment = Comment.objects.get(pk=comment_pk)
    return render(request, 'news/post_view_comment_perma.html', {'post': post, 'comment': comment})




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

@login_required
def comment_vote(request):
    if request.method == 'POST':
        comment_id = request.POST.get('commentid')
        comment = Comment.objects.get(pk=comment_id)
        if CommentVote.objects.filter(comment=comment, user=request.user).exists():
            c = CommentVote.objects.get(comment=comment, user=request.user)
            c.delete()
            comment.score -= 1
            comment.save()
            return HttpResponse('removed')
        else:
            c = CommentVote(comment=comment, user=request.user)
            c.save()
            comment.score += 1
            comment.save()
            return HttpResponse('added')
    else:
        return HttpResponse('')
