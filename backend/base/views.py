from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.conf import settings as conf_settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from datetime import date

from base.models import *

import json
import datetime
import requests

# Create your views here.
@api_view(['POST'])
def addEmail(request):
    data = request.data
    try:
        email = Email.objects.create(
            name = data['name'],
            email = data['email']
        )
        return Response({
            'message':'You have successfully subscribed to email list'
            })
    except:
        return Response({
            'message':'Email already subscribed'
            })

@api_view(['POST'])
def removeEmail(request):
    data = request.data
    try:
        email = Email.objects.get(email = data['email'])
        return Response({
            'message':'You have successfully usubscribed from the email list'
            })
    except:
        return Response({
            'message':'Email was not found'
            })


