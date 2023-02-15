import django
from django.db import models
import datetime
# Create your models here
ACCOUNT_CHOICES = [
        ('BUSSINESS', 'BUSSINESS'),
        ('PERSONAL', 'PERSONAL'),
    ]
class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images',default='')
    account_type = models.CharField(max_length=50,choices=ACCOUNT_CHOICES,default='PERSONAL')
    contact_number = models.IntegerField(default=None)
    passion = models.CharField(max_length=100,default=None)
    points = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)
    profile_dp = models.ImageField(default='')
    created_date = models.DateField(default=django.utils.timezone.now)


class Products(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/',default='')
    building_name = models.CharField(max_length=100)
    latitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    upload_date = models.DateField(default=django.utils.timezone.now)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    subcribers = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
class Review(models.Model):
    Product = models.ForeignKey(Products,on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    comment_by =models.ForeignKey(Users,on_delete=models.CASCADE)
    posted_date = models.DateField(default=django.utils.timezone.now)

class HowToUseDB(models.Model):
    username = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    show = models.CharField(max_length=50, choices=[(True,True),(False,False)],default=True)

class LiveDB(models.Model):
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100,default='')
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    streaming_id = models.CharField(max_length=50)
    live = models.CharField(max_length=50,choices=[(True,True),(False,False)])