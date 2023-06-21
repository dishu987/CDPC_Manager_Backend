from django.contrib import admin
from .models import UserModel,RoleGroup


admin.site.register(UserModel)
admin.site.register(RoleGroup)