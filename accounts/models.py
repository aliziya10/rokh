from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save



class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=50, unique=True, blank=False, null=False)
    pezeshki_code = models.IntegerField(verbose_name='شماره نظام پزشکی', blank=True, null=True, )
    email = models.EmailField(unique=False, max_length=50, blank=True, null=True, default=None)
    phone = models.BigIntegerField(verbose_name='موبایل', blank=True, null=True, )
    last_login = models.DateTimeField(_("last login"), default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["name", 'password']

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    Bio = models.TextField(null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)

    def __str__(self):
        return self.user.username

def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()



post_save.connect(save_profile_user,sender=User)