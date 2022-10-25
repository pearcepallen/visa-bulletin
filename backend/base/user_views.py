from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework.response import Response

from django.contrib.auth.models import User
from base.models import *
from base.serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        #makeshift way to stop default refresh & access token from popping up | double check for issues
        # del data['refresh']
        # del data['access']

        data['message'] = 'Successfully logged in'
        data['code'] = '0'

        serializer = UserSerializerWithToken(self.user).data
        obj = {}
        for k, v in serializer.items():
            obj[k] = v
        data['jwt'] = obj['token']

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['firstName'],
            last_name=data['lastName'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({
        'message':'User logged out successfully',
        'code' : 0
        })
    except:
        return Response({
        'message':'Bad request',
        'code' : 1
        })