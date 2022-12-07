from django.core.mail import EmailMessage, send_mail
from django.conf import settings as conf_settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import *

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse

from datetime import date
import datetime
import requests

# Create your views here.
@api_view(['POST'])
def createEmail(request):
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
def deleteEmail(request):
    data = request.data
    try:
        email = Email.objects.get(email = data['email'])
        email.delete()
        return Response({
            'message':'You have successfully usubscribed from the email list'
            })
    except:
        return Response({
            'message':'Email was not found'
            })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEmails(request):
    emailList = []
    emails = Email.objects.all()
    for email in emails:
        emailList.append(email.email)
    return Response({
        'Emails': emailList,
    })

@api_view(['GET'])
def getBulletin(request):
        currentBulletin = None
        defaultString = 'https://travel.state.gov/content/dam/visas/Bulletins/visabulletin_%20October2022.pdf'
        today = date.today()
        nextMonthDate = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        nextMonth = nextMonthDate.strftime('%B')
        nextMonthYear = nextMonthDate.strftime('%Y')
        upcomingDate = nextMonth+nextMonthYear
        
        try:
            currentBulletin = Bulletin.objects.get(month=nextMonth, year=nextMonthYear)
        except Bulletin.DoesNotExist:
            currentBulletin = None
        
        if not currentBulletin:
            upcoming = defaultString.replace('October2022', upcomingDate)
            pdf = requests.get(upcoming)
            if pdf.status_code != 404:
                sendEmail(pdf.content, nextMonthDate)
                Bulletin.objects.create(
                    month=nextMonth,
                    year=nextMonthYear, 
                )
                return Response({
                    'message': 'Bulletin sent',
                })
            else:
               return Response({
                    'message': 'Visa Bulletin not found',
                }) 
        else:
            return Response({
                'message': 'Bulletin was already sent',
            })

def sendEmail(content, date):
    emailList = []
    emails = Email.objects.all()
    for email in emails:
        emailList.append(email.email)
    name = f'Visa Bulletin {date.strftime("%B %Y")}'
    email = EmailMessage(
        name,
        f'Please see attached for {name}.',
        'from@example.com',
        emailList,
    )
    email.attach(f'{name}.pdf', content)
    email.send(fail_silently=False)

