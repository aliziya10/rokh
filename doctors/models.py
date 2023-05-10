from django.db import models






class Doctor(models.Model):
    name=models.CharField(max_length=30)
    mobile=models.CharField(max_length=20)