from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
import base64
import hmac
import hashlib
import urllib.parse as urllib
from django.contrib.auth.decorators import login_required
from django.conf import settings
from urllib.parse import parse_qs


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

@login_required
def sso(request):
    payload = request.GET.get('sso')
    signature = request.GET.get('sig')

    if None in [payload, signature]:
        return HttpResponseBadRequest('No SSO payload or signature. Please contact support if this problem persists.')

    ## Validate the payload

    try:
        payload = bytes(urllib.unquote(payload), encoding='utf-8')
        decoded = base64.decodestring(payload).decode('utf-8')
        assert 'nonce' in decoded
        assert len(payload) > 0
    except AssertionError:
        return HttpResponseBadRequest('Invalid payload. Please contact support if this problem persists.')

    key = bytes(settings.DISCOURSE_SSO_SECRET, encoding='utf-8') # must not be unicode
    h = hmac.new(key, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        return HttpResponseBadRequest('Invalid payload. Please contact support if this problem persists.')

    ## Build the return payload

    qs = parse_qs(decoded)
    params = {
        'nonce': qs['nonce'][0],
        'email': request.user.email,
        'external_id': request.user.id,
        'username': request.user.username,
        'require_activation': 'true',
    }

    return_payload = base64.encodestring(bytes(urllib.urlencode(params), 'utf-8'))
    h = hmac.new(key, return_payload, digestmod=hashlib.sha256)
    query_string = urllib.urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    ## Redirect back to Discourse

    url = '%s/session/sso_login' % settings.DISCOURSE_BASE_URL
    return HttpResponseRedirect('%s?%s' % (url, query_string))
