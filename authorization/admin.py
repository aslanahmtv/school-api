from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
admin.site.register(models.User)