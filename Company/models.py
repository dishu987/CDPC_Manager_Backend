from django.db import models
from django.contrib.auth.models import User
from users.models import UserModel


class HRDetails(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='hr_details')


class Comment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CompanyTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    assigned_coordinators = models.ManyToManyField(UserModel, related_name='assigned_companies')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    importance = models.IntegerField()
    years_of_collaboration = models.IntegerField()
    spoc = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    job_location = models.CharField(max_length=300  )
    hr_details = models.ManyToManyField(HRDetails, related_name='companies')
    blacklist = models.BooleanField(default=False)
    tags = models.ManyToManyField(CompanyTag, related_name='related_tags')


    def __str__(self):
        return self.name
    