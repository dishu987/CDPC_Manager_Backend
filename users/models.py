from django.db import models
from .utils.options.genders import GENDERS_OPTIONS
from .managers.user import UserManager
import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
import uuid
from django.utils import timezone
import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User



class RoleGroup(models.Model):
    role = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.role
    

class UserModel(AbstractBaseUser, PermissionsMixin): 
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True,)
    name = models.CharField(max_length=200)
    role_group = models.ForeignKey(RoleGroup,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='assigned_roles',verbose_name='assigned_roles')
    mobile = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=100,choices=GENDERS_OPTIONS,null=True,blank=True)
    address = models.CharField(max_length=500,default="NA",null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # we can add field later also ie profile_img etc
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']
    def __str__(self):
        return self.email+"/Role : "+str(self.role_group)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
