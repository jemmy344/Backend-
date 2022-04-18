from ast import Return
from django import http
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from urllib.parse import urlparse
import json
from .models import RegisteredSites
import requests
import re
from bs4 import BeautifulSoup

from django.views.decorators.csrf import csrf_exempt



def cookieChecker(url):
  response = requests.get(url)
  

  cookies = response.cookies
  if cookies: 
    return True
  return False

def checker(url): 
  source = requests.get(url).text
  soup = BeautifulSoup(source, "lxml")

  search = soup.findAll(text=re.compile('cookies'))

  for i in search:
    soup = i.parent.text
    if ("accept" in soup or "Accept" in soup or "Allow" in soup or "allow" in soup):
      return True


  search1 = soup.findAll("a")
  for i in search1:
    link = i.text
    if ("privacy" in link or "policy" in link or "Privacy" in link or "Policy" in link) : 
      return True
    
  #print(search)
  return False 
  
  


@csrf_exempt
def checkurl(requests):
	if requests.method != 'POST':
		return HttpResponse('Invalid method', 403)
	print(requests.POST.get('name'))
	data = json.loads(requests.body)
	url = data.get('url')
	uri = urlparse(url)
	
	if not (uri.scheme or uri.netloc):
		return JsonResponse({'code':500, 'status':'error', 'message': 'invalid url. url must contain url scheme and domain'})
    
	# obj, created = RegisteredSites.objects.get_or_create(
	# 	url = uri.netloc,
	# 	defaults = {
	# 		# 'url':uri.netloc,
	# 		'has_cookie':cookieChecker(url)
	# 	}
	
	# )
	
	checker(url)
	response = JsonResponse({'code':200,'status':'success','has_cookie':cookieChecker(url), 'privacy_policy': cookieChecker(url) and checker(url) })
	return response
