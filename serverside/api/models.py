from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Charity(models.Model):
    charity_name = models.CharField(max_length=128)
    description = models.TextField()
    charity_contact_name = models.CharField(max_length=64)
    charity_contact_email = models.CharField(max_length = 128)
    charity_contact_phone = models.CharField(max_length = 64)

    def __str__(self):
        return 'Charity: {}'.format(self.charity_name)

    def update_stats(self):
        """add new rounded up transactions to User's db"""


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
    category_charities = models.ManyToManyField(Charity)

    def __str__(self):
        return 'Category: {}'.format(self.category_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_joined = models.DateField(auto_now_add=True)
    is_donator = models.BooleanField(default=False)  #True if Plaid+Stripe account setup done
    user_categories = models.ManyToManyField(Category)
    user_charities = models.ManyToManyField(Charity)

    stripe_customer_id = models.CharField(max_length=64)
    plaid_customer_id = models.CharField(max_length=64)

    def __str__(self):
        return 'Profile: {}'.format(self.user)


class Transactions(models.Model):
    """Plaid required. Set Profile.is_donator = True if user authorized thru Plaid/Stripe"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.CharField(max_length = 64, default ='100')
    date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return 'Donator: {}'.format(self.user)