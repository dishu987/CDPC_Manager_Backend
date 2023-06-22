from django.contrib import admin
from .models import Comment,CompanyTag,Company,HRDetails

# Register your models here.
admin.site.register(HRDetails)
admin.site.register(CompanyTag)
admin.site.register(Company)
admin.site.register(Comment)
