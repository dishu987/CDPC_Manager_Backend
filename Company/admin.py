from django.contrib import admin
from .models import Comment,Company,HRDetails,Feedback,CompanyJobTag,CompanyHiringTag

# Register your models here.
admin.site.register(HRDetails)
admin.site.register(CompanyHiringTag)
admin.site.register(CompanyJobTag)
admin.site.register(Company)
admin.site.register(Comment)
admin.site.register(Feedback)
