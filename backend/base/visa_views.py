from django.core.mail import EmailMessage, send_mail
from django.conf import settings as conf_settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import *

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


