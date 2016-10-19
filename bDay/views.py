from django.shortcuts import render, redirect
from django.conf import settings

from .models import Credentials

import urllib, requests, datetime, pytz

import os
# import logging
# logger = logging.getLogger(__name__)


def index(request):
  params = { 'redirect_uri' : os.environ['REDIRECT_URI'], 'response_type' : "code", 'client_id' : os.environ['CLIENT_ID']}
  encoded = urllib.urlencode(params)
  fullurl = 'https://drchrono.com/o/authorize/?' + encoded

  context = {'appname': 'v0.01', 'redirect_uri': fullurl}

  return render(request, 'bDay/index.html', context)


def save_tokens(request):
  # if request.GET['error']:
  #     raise ValueError('Error authorizing application: %s' % request.GET['error'])

  if Credentials.objects.latest('expires_date').expires_date > datetime.datetime.now(pytz.utc):
    return redirect('/patients')

  response = requests.post('https://drchrono.com/o/token/', data={
    'code': request.GET['code'],
    'grant_type': 'authorization_code',
    'redirect_uri': os.environ['REDIRECT_URI'],
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['CLIENT_SECRET']
  })
  response.raise_for_status()
  data = response.json()
  
  # Save these in your database associated with the user
  access_token = data['access_token']
  refresh_token = data['refresh_token']
  expires_date = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

  entry = Credentials(access_token=access_token, refresh_token=refresh_token,expires_date=expires_date)
  entry.save()
  context = {'access_token': access_token, 'refresh_token': refresh_token, 'expires_date': expires_date}
  return render(request, 'bDay/loggedIn.html', context)


def patients(request):
  token = Credentials.objects.latest('expires_date').access_token
  headers = {'Authorization': 'Bearer %s' % token}

  patients = []
  patients_url = 'https://drchrono.com/api/patients'
  while patients_url:
      data = requests.get(patients_url, headers=headers).json()
      patients.extend(data['results'])
      patients_url = data['next'] # A JSON null on the last page

  return render(request, 'bDay/patients.html', {'patients': patients})    

