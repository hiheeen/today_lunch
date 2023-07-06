from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractBaseUser,PermissionsMixin):
    user_name_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=15)
    userId = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField()

    objects = UserManager()

    USERNAME_FIELD = 'userId' # 로그인 시 필요