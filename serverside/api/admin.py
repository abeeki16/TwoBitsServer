from django.contrib import admin

# Register your models here.

from .models import Profile, Charity

admin.site.register(Profile)
admin.site.register(Charity)

