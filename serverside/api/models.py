from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_joined = models.DateField(auto_now_add=True)


class Charity(models.Model):
    charity_name = models.CharField(max_length=128)
    description = models.TextField()
    charity_contact_name = models.CharField(max_length=64)
    charity_contact_email = models.CharField(max_length = 128)
    charity_contact_phone = models.CharField(max_length = 64)
    charity_category = models.CharField(max_length=128)
    charity_donators = models.ManyToManyField(Profile)


class Category(models.Model):
    category_name = models.CharField(max_length=128)
    category_charities = models.ManyToManyField(Charity)
    category_donators = models.ManyToManyField(Profile)

