from calendar import month
from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models

class Bulletin(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    month = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('month', 'year')

class Email(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=False, unique=True)

