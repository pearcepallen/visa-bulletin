from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.conf import settings as conf_settings

from datetime import date

import json
import datetime
import requests

# Create your views here.

def getBulletin(request):
    defaultString = 'https://travel.state.gov/content/dam/visas/Bulletins/visabulletin_%20October2022.pdf'
    today = date.today()
    nextMonthDate = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    nextMonth = nextMonthDate.strftime('%B')
    nextMonthYear = nextMonthDate.strftime('%Y')
    upcomingDate = nextMonth+nextMonthYear
    upcoming = defaultString.replace('October2022', upcomingDate)
    pdf = requests.get(upcoming)
    if pdf:
        if pdf.status_code != '404':
            sendEmail(pdf.content, nextMonthDate)
    # sendEmail(pdf.content, nextMonthDate)
    # return HttpResponse(status=404)
    return JsonResponse("Good", safe=False)

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


