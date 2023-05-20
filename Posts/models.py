from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Value, F, CharField
from django.db.models.functions import Concat
from django.utils import timezone
from accounts.models import User
from django.utils.translation import gettext_lazy as _
import jdatetime


# tags=models.ManyToManyField(Tag,related_name="tagname",editable=True)

def validate1or2(value):
    if value!=1 and value!=0:
        raise ValidationError(
            _('%(value)s is not 0 or 1'),
            params={'value': value},
        )



class Post(models.Model):
    title = models.CharField(max_length=80,blank=False,null=True)
    sub_title=models.CharField(max_length=80,null=False)
    text=models.TextField()
    # image = models.ImageField(blank=True,null=True,default="default.png")
    status=models.IntegerField(validators=[validate1or2],null=False)
    dateOfPublish = models.DateTimeField(default=timezone.now,editable=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    persian_date = models.CharField(max_length=10, blank=True, null=True,editable=False)
    image_url = models.TextField(null=True)



    def __str__(self):
        return self.title



    def save(self, *args, **kwargs):
        if self.dateOfPublish and not self.persian_date:
            jalali_date = jdatetime.date.fromgregorian(date=self.dateOfPublish)
            self.persian_date = jalali_date.strftime('%Y/%m/%d')
        super(Post, self).save(*args, **kwargs)

    class Meta:
        permissions = [
            ('access', 'Can access'),
        ]





class Tag(models.Model):
    tag = models.CharField(blank=False,unique=True,max_length=25)
    post_id=models.ManyToManyField(Post)


    def meetings_list(self):
        return ", ".join([m.meeting_name for m in self.tag.all()])

    def __str__(self):
        return self.tag


class ImagePost(models.Model):
    image=models.ImageField(upload_to='post/',null=False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url





class Comments(models.Model):
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)
    # user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="id")
    text=models.TextField()
    parent_id=models.IntegerField(default=0,null=True)

