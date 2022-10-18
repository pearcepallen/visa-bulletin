from calendar import month
from django.db import models

class Bulletin(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    month = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)

# Create your models here.
