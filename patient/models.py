from django.db import models
from accounts.models import User


# class Patient(models.Model):
#     name=models.CharField(max_length=50,null=False)
#     code=models.CharField(max_length=20)
#     doctor=models.ForeignKey(User,on_delete=models.CASCADE)
#     image=models.ImageField(upload_to='patient/',null=True,blank=True)
#
#
#     def __str__(self):
#         return self.name