from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

