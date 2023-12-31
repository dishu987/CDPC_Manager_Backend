from django.db import models
from django.contrib.auth.models import User
from users.models import UserModel
from django.utils import timezone



class CompanyHiringTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class CompanyJobTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class HRDetails(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    


class Company(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField(default="NA",null=True,blank=True)
    assigned_coordinators = models.ManyToManyField(UserModel, related_name='assigned_companies')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    importance = models.IntegerField()
    years_of_collaboration = models.IntegerField()
    spoc = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    job_location = models.CharField(max_length=300  )
    hr_details = models.ManyToManyField(HRDetails, related_name='companies')
    blacklist = models.BooleanField(default=False)
    job_tags = models.ManyToManyField(CompanyJobTag, related_name='job_tags')
    hiring_tags = models.ManyToManyField(CompanyHiringTag, related_name='hiring_tags')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Comment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "text: "+self.text+" /to: "+str(self.company)+" /by: "+str(self.user)
    


class Feedback(models.Model):
    hr = models.ForeignKey(HRDetails,on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.company)+"/ hr: "+str(self.hr)
    

    