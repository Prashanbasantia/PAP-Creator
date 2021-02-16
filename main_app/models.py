from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings

# Create your models here.
class Category_prod(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class products(models.Model):
    id=models.AutoField(primary_key=True)
    cate_id=models.ForeignKey(Category_prod,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    unity = models.IntegerField()
    price = models.CharField(max_length=128, blank=True,default='0000')
    quantity = models.IntegerField(default=0,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Customer"))
    profile_photo =models.ImageField(upload_to='customer_photo/')
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    dob=models.CharField(max_length=100)
    address=models.TextField()
    is_verify = models.BooleanField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Receipt(models.Model):
    id=models.AutoField(primary_key=True)
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    prod_id=models.ForeignKey(products,on_delete=models.CASCADE)
    prod_quantity = models.CharField(max_length=100)
    receipt_type = models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Img(models.Model):
    profile_photo =models.ImageField(upload_to='image/')
    objects=models.Manager()

class Otp(models.Model):
    otp = models.IntegerField()
    cust_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    objects=models.Manager()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Customer.objects.create(admin=instance,dob="",address="")
        
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.customer.save()
    
    