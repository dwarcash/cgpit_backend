from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, enroll_no, email, password=None):

        if enroll_no is None:
            raise TypeError('Enrollment No. cannot be blank !')

        if email is None:
            raise TypeError('Email cannot be blank !')

        user = self.model(enroll_no=enroll_no,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, enroll_no, email, password=None):

        if password is None:
            raise TypeError('Password cannot be blank !')

        user = self.create_user(self, email, password)
        user = self.model(email=self.normalize_email(email))
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = None
    enroll_no = models.CharField(max_length=15, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    # user_type = models.CharField(max_length=8, default='student')
    # branch = models.CharField(max_length=8, null=True)
    # section = models.CharField(max_length=1, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'enroll_no'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.enroll_no

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
