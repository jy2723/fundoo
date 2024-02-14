from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
import re

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password','first_name','last_name','date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['date_joined']
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        email = attrs.get('email')

        if len(username) <= 3:
            raise serializers.ValidationError("Username must be greater than 3 characters.")

        if len(password) < 8 or not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>?]', password):
            raise serializers.ValidationError("Password must be at least 8 characters long and contain at least one special character.")

        
        if "@" not in email:
            raise serializers.ValidationError("Email must contain the @ symbol.")

        # validation logic
        return super().validate(attrs)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True, write_only=True)
    password = serializers.CharField(max_length=50, required=True, write_only=True)
    
    
    def create(self, validate_data):
        user = authenticate(**validate_data)
        if not user:
            raise exceptions.AuthenticationFailed('Invalid username or password')
        return user