from django.db import models


class RegisteredSites(models.Model):
    url = models.CharField(max_length=200)
    has_cookie = models.BooleanField()

# Create your models here.
