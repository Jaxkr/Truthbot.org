from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def post_list(request):
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
