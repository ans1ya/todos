from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todos(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    task_name=models.CharField(max_length=100)
    completed_status=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)