from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, userId, password=None):        

        user = self.model(            
            username = username,            
            userId = userId,        
        )        
        user.set_password(password)        
        user.save(using=self._db)        
        return user
    
    def create_superuser(self,username, userId, password=None):
        user = self.create_user(
            username = username,            
            userId = userId,
            password = password  
        )
        user.is_admin = True        
        user.is_superuser = True        
        user.is_staff = True        
        user.save(using=self._db)        
        return user 




# def create_user(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(username, email, password, **extra_fields)

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    user_name_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=15)
    userId = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField()

    objects = UserManager()

    USERNAME_FIELD = 'userId' # 로그인 시 필요
    REQUIRED_FIELDS = ['username']