from django.db import models
from users.models import UserModel
from Company.models import Company

class Internship(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    start_date = models.DateField()
    end_date = models.DateField()
    is_remote = models.BooleanField(default=False)

    def __str__(self):
        return self.title


