from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# UserAdmin gives the usual user pages (password hashing, permissions, etc.).
admin.site.register(User, UserAdmin)
