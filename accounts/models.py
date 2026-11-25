from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from enums import UserRole

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email: raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra):
        extra.update(is_staff=True, is_superuser=True, role=UserRole.ADMIN)
        return self.create_user(email, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']
    def get_age(self):
        if not self.birth_date: return None
        today = date.today()
        return today.year-self.birth_date.year-((today.month,today.day)<(self.birth_date.month,self.birth_date.day))
    def __str__(self): return self.email
