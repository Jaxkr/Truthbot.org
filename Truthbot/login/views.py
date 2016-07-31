from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test


def user_is_not_logged_in(user):
    return not user.is_authenticated()


# Create your views here.

@user_passes_test(user_is_not_logged_in, login_url='organizationroot', redirect_field_name=None)
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #create the user!
            try:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
                user_auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                auth_login(request, user_auth)
                return HttpResponseRedirect(reverse('organizationroot'))
            except:
                form.add_error('username', 'Username already taken!')
                return render(request, 'login/register.html', {'form': form})
        else:
            #there was a problem, return the form again
            return render(request, 'login/register.html', {'form': form})

    #runs when we aren't using post
    form = RegistrationForm()
    return render(request, 'login/register.html', {'form': form})

@user_passes_test(user_is_not_logged_in, login_url='organizationroot', redirect_field_name=None)
def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user_auth is not None:
                auth_login(request, user_auth)
                return HttpResponseRedirect(request.POST.get('next') or '/')
            else:
                form.add_error(None, 'Username or password incorrect.')
                return render(request, 'login/login.html', {'form': form})
        else:
            return render(request, 'login/login.html', {'form': form})

    form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
