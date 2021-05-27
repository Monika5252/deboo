from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User

class User(AbstractUser):
    username = models.CharField(blank=True, max_length=60, null=True)
    email = models.EmailField(_('email address'), blank=True, max_length=60)
    mobile = models.CharField(max_length=15,unique=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.mobile)
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=55,blank=True)
    birthdate = models.CharField(max_length=20,blank=True)
    age = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=255,blank=True)
    country = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    zip = models.CharField(max_length=7,blank=True)
    photo = models.CharField(blank=True,max_length=500)


class Feedback(models.Model):
    mobile = models.CharField(max_length=15, blank=False)
    rate = models.CharField(max_length=5,blank=True)
    text = models.CharField(max_length=255,blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return "{}".format(self.mobile)

class ContactUs(models.Model):
    contact = models.CharField(max_length=30, blank=False)
    mobile = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return "{}".format(self.contact)