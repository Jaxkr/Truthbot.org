from django.shortcuts import render

# Create your views here.

def article(request, url):
    return render(request, 'public/article.html')
