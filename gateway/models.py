from os import access
from django.db import models
from user.models import CustomUser #refrence from the user
# Create your models here.
class JWT(models.Model):
    user = models.OneToOneField(CustomUser, related_name='login_user', on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)