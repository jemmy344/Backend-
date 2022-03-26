from ast import Return
from email.policy import default
from django import http
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from urllib.parse import urlparse
import json
from .models import RegisteredSites
import requests

from django.views.decorators.csrf import csrf_exempt



def cookieChecker(url):
  response = requests.get(url)
  

  cookies = response.cookies
  if cookies: 
    return True
  return False
  
  


@csrf_exempt
def checkurl(requests):
    if requests.method != 'POST':
        return HttpResponse('Invalid method', 403)
    data = json.loads(requests.body)
    url = data.get('url')
    uri = urlparse(url)

    if not (uri.scheme or uri.netloc):
        return JsonResponse({'code':500, 'status':'error', 'message': 'invalid url. url must contain url scheme and domain'})
    
    obj, created = RegisteredSites.objects.get_or_create(
        url = uri.netloc,
        defaults = {
            # 'url':uri.netloc,
            'has_cookie':cookieChecker(url)
        }

    )
    

    response = JsonResponse({'code':200,'status':'success','has_cookie':obj.has_cookie})
    return response
