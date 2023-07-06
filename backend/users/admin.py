from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("User Info", {"fields": ("username", "userId", "password")}),
    )

    list_display = ('username',"userId")