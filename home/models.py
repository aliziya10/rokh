from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _




def validate1or2(value):
    if value!=1 and value!=0:
        raise ValidationError(
            _('%(value)s is not 0 or 1'),
            params={'value': value},
        )




class RokhInfo(models.Model):
    name=models.CharField(max_length=30)
    number=models.CharField(max_length=20)
    address=models.CharField(max_length=80)
    description=models.TextField()
    email=models.EmailField(default="hanousa@gmail.com")
    image=models.ImageField(null=True)
    image_url = models.TextField(null=True,blank=True)
    score=models.FloatField(max_length=3,default=4.7)
    services=models.IntegerField(default=100)


    def __str__(self):
        return self.name




class Menu(models.Model):
    title=models.CharField(db_index=True,max_length=25,null=False)
    link=models.CharField(max_length=150, null=True,blank=True,default="#")
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image_url="https://storage.iran.liara.space/hanousa/static/"+self.image.name

    def __str__(self):
        return str(self.id)

    def imagepath(self):
        return self.image.path


class ContactUs(models.Model):
    name = models.CharField(db_index=True, max_length=50, unique=False, blank=False, null=False)
    mobile = models.CharField(max_length=50, unique=False, blank=False, null=False)
    email = models.EmailField(unique=False, max_length=50, blank=False, null=False)
    comment = models.TextField(max_length=500, blank=False, null=False)
    is_answer = models.BooleanField(default=False, editable=True)

    def __str__(self):
        return self.name

    def shortcomment(self):
        return self.comment[:50] + " ..."



class TicketAnswer(models.Model):
    answer = models.TextField(max_length=500, blank=False, null=False)
    name = models.CharField(max_length=30)
    ticket_id = models.OneToOneField(ContactUs, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer[:20] + " ..."