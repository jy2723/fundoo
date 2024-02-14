from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
from .models import User
from django.forms import model_to_dict
from rest_framework.views import APIView
from .serializer import RegisterSerializer
from .serializer import LoginSerializer
from rest_framework.response import Response

# Create your views here.
class UserAPI(APIView):    
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({'message': 'User registered', 'status': 201, 'data': serializer.data},status=201)
        except Exception as e:
            return JsonResponse({'message': str(e), 'status': 400},status=400)

class LoginAPI(APIView): 
    def post(self,request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Login successful', 'status': 200}, status=200)
        # User authentication failed
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data in request body', 'status': 400})
        except Exception as e:
            return JsonResponse({'message': str(e), 'status': 400})