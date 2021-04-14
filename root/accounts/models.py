from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# class MyAccountManager(BaseUserManager):
#     def create_user(self,email,username,password=None):
#         if not email:
#             raise ValueError("user error mail")
#         if not username:
#             raise ValueError("user error name")
        
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#         def create_superuser(self,email,username,password):
#             user = self.create_user(
#                 email=self.normalize_email(email),
#                 password=password,
#                 username=username,
#             )
#             user.is_admin = True
#             user.is_staff = True
#             user.is_superuser = True
#             user.save(using=self._db)
#             return user



# class Account(AbstractBaseUser):
#     email = models.EmailField(verbose_name="email ",max_length=100 , unique=True)
#     username= models.CharField(max_length=30 , unique=True)
#     is_active= models.BooleanField(default=True)
#     # password=models.CharField(max_length=30)
#     # USERNAME_FIELD='email'
#     # REQUIRED_FIELDS=['username']
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     objects = MyAccountManager()

#     # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
#     # def create_auth_token(sender, instance=None, created=False, **kwargs):
#     #     if created:
#     #         Token.objects.create(user=instance)











