from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Credentials(models.Model):
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_date = models.DateTimeField('expire time')