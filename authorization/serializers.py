from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'id', 'is_active', 'is_staff', 'groups', 'user_permissions', 'activation_date',
                   'verification_str', 'last_login', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegisterSerializer, self).create(validated_data)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}