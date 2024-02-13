from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=20,null=False,unique=True)
    email = models.EmailField(max_length=254,null=False)
    passwaord = models.CharField(max_length=50,null=False)
    location = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    

    
