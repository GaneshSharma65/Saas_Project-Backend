from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
