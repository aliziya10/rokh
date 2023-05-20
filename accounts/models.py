from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save


class CustomUser(BaseUserManager):
    def _create_user(self, username, password, email, **extra_fields):
        if not username:
            raise ValueError("username must be provided")

        if not password:
            raise ValueError("Password is not provided")

        if email != "":

            user = self.model(
                username=username,
                email=self.normalize_email(email)
                , **extra_fields,
            )

        else:
            user = self.model(
                username=username,
                **extra_fields,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_doctor', False)
        return self._create_user(username, password, email, **extra_fields)

    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_doctor', True)

        # extra_fields.setdefault("is_admin",True)
        return self._create_user(username, password, email, **extra_fields)

    def __str__(self):
        return str(self.mobile)

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(db_index=True, max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(unique=False, max_length=50, blank=True, null=True, default=None)
    phone = models.TextField(verbose_name='موبایل', blank=True, null=True, )
    last_login = models.DateTimeField(_("last login"), default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_doctor=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email",'password']
    objects = CustomUser()
    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Expertise(models.Model):
    name = models.CharField(max_length=100,unique=True)


    def __str__(self):
        return self.name


class Example(models.Model):
    text=models.TextField(null=True)
    image=models.ImageField(null=True)
    expertise=models.ForeignKey(Expertise,on_delete=models.CASCADE)
    doctor=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.doctor.username+' : '+self.text[:20]





class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pezeshki_code = models.IntegerField(verbose_name='شماره نظام پزشکی', blank=True, null=True, )
    name=models.CharField(max_length=50,null=True,blank=True)
    working_hour=models.TextField(null=True,max_length=120)
    bio = models.TextField(null=True,blank=True)
    birth_year = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)
    expertise=models.ManyToManyField(Expertise)


    def __str__(self):
        return self.user.username

def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()



post_save.connect(save_profile_user,sender=User)