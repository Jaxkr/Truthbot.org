from django.shortcuts import render
from django.http import HttpResponse

from .forms import *

# Create your views here.

def register(request):
    registrationForm = RegistrationForm()

    return render(request, 'login/register.html', {'form': registrationForm})
