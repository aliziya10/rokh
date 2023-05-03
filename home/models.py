from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _




def validate1or2(value):
    if value!=1 and value!=0:
        raise ValidationError(
            _('%(value)s is not 0 or 1'),
            params={'value': value},
        )




class HanousaInfo(models.Model):
    name=models.CharField(max_length=30)
    number=models.CharField(max_length=20)
    address=models.CharField(max_length=80)
    description=models.TextField()
    email=models.EmailField(default="hanousa@gmail.com")
    image=models.ImageField(null=True)
    image_url = models.TextField(null=True)

    def __str__(self):
        return self.name




class Menu(models.Model):
    title=models.CharField(db_index=True,max_length=25,null=False)
    link=models.CharField(max_length=150,null=True,blank=True,default="#")
    parent_id=models.IntegerField(default=0,editable=True)
    type=models.CharField(max_length=20,null=False,default="header")


    def __str__(self):
        return str(self.title)+" "+str(self.id)






class Slides(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField()
    image=models.ImageField(null=True)
    status=models.IntegerField(validators=[validate1or2],null=False)
    image_url=models.TextField(null=True,max_length=1000)


    def __str__(self):
        return self.title

    def imagepath(self):
        return self.image.url


class Teammate(models.Model):
    image=models.ImageField(null=False)
    link=models.TextField(default="#",null=True)
    label=models.CharField(max_length=30)
    image_url = models.TextField(null=True)


    def __str__(self):
        return str(self.id)

    def imagepath(self):
        return self.image.path

