from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Charity(models.Model):
    charity_name = models.CharField(max_length=128)
    description = models.TextField()
    charity_contact_name = models.CharField(max_length=64)
    charity_contact_email = models.CharField(max_length = 128)
    charity_contact_phone = models.CharField(max_length = 64)
    charity_category = models.CharField(max_length=128)

class Category(models.Model):
    Health = 'Health'
    Education = 'Education'
    AnimalRights = 'Animal Rights'
    Other = 'Other'
    CATEGORY_CHOICES = (
        (Health, 'Health'), (Education, 'Education'), (AnimalRights, 'Animal Rights'), (Other, 'Other'),
    )
    category_name = models.CharField(max_length=128, choices=CATEGORY_CHOICES, default=Other,)
    description = models.TextField(default='')
    category_charities = models.ManyToManyField(Charity, blank = True)

    def __str__(self):
        return 'Category: {}'.format(self.category_name)



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_joined = models.DateField(auto_now_add=True)
    charities = models.ManyToManyField(Charity,blank=True)
    categories = models.ManyToManyField(Category, blank=True)
