from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.conf import settings as conf_settings

from datetime import date

from base.models import *

import json
import datetime
import requests

# Create your views here.

def getBulletin():
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
            if pdf.status_code != '404':
                sendEmail(pdf.content, nextMonthDate)
                Bulletin.objects.create(
                    month=nextMonth,
                    year=nextMonthYear, 
                )

def sendEmail(content, date):
    emailList = json.loads(conf_settings.EMAIL_LIST)
    name = f'Visa Bulletin {date.strftime("%B %Y")}'
    email = EmailMessage(
        name,
        f'Please see attached for {name}.',
        'from@example.com',
        emailList,
    )
    email.attach(f'{name}.pdf', content)
    email.send(fail_silently=False)