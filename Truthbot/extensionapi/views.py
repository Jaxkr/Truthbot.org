from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

from dashboard.models import *
# Create your views here.


def get_site_info(request):
	data = {'test': 'test'}
	response = JsonResponse(data)
	response['Access-Control-Allow-Origin'] = '*'
	return response