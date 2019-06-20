from django.contrib import admin

# Register your models here.
from django.contrib.admin import site

from user.models import User

admin.site.register(User)
