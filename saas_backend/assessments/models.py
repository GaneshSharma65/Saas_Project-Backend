from django.db import models
from students.models import Student  
# Create your models here.
class Assessment(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    week = models.IntegerField()
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
