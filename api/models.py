from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

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
    gender = models.CharField(max_length=8,blank=True)
    city = models.CharField(max_length=50,blank=True)
    zip = models.CharField(max_length=7,blank=True)
    photo = models.CharField(blank=True,max_length=500)


class Feedback(models.Model):
    mobile = models.CharField(max_length=15, blank=False)
    rate = models.CharField(max_length=5,blank=True)
    text = models.CharField(max_length=255,blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    createdAt = models.DateField(default=datetime.date.today)
    updatedAt = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{}".format(self.mobile)

class ContactUs(models.Model):
    contact = models.CharField(max_length=30, blank=False)
    mobile = models.CharField(max_length=15,blank=True)
    createdAt = models.DateField(default=datetime.date.today)
    updatedAt = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{}".format(self.contact)


class Setup(models.Model):
    name = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=255, blank=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    country = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    fees = models.IntegerField()
    occupyTime = models.IntegerField(blank=True, null=True, default=10)
    zip = models.CharField(max_length=7,blank=True)
    photo = models.CharField(blank=True,null=True,max_length=500)
    isOccupied = models.BooleanField(default=False, blank=True)
    isCleaned = models.BooleanField(default=True, blank=True)
    createdBy = models.CharField(blank=True, max_length=4)
    updatedBy = models.CharField(blank=True, max_length=4)
    occupiedBy = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name='users')
    createdAt = models.DateField(default=datetime.date.today)
    updatedAt = models.DateField(default=datetime.date.today)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=30, blank=False)
    money = models.IntegerField(blank=False)
    date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, related_name='user')
    setup = models.ForeignKey(Setup, on_delete = models.CASCADE, blank = True, related_name='setup')
    createdAt = models.DateField(default=datetime.date.today)
    updatedAt = models.DateField(default=datetime.date.today)

class Notification(models.Model):
    text = models.CharField(max_length=255, blank=False)
    isRead = models.BooleanField(default=False)
    createdAt = models.DateField(default=datetime.date.today)
    updatedAt = models.DateField(default=datetime.date.today)
    setup = models.ForeignKey(Setup, on_delete = models.CASCADE, blank = True, related_name='setups')
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, related_name='userss')

