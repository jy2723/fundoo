from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    
class RequestLog(models.Model):
    method = models.CharField(max_length=10, null=False)
    path = models.CharField(max_length=255, null=False)
    count = models.BigIntegerField(default=1)


    
