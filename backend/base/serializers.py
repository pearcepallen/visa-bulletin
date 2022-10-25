from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken
from . models import *


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ['name',]



class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'email', 'groups']

    def get_id(self, obj):
        return obj.id



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)