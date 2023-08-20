from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')


    avatar = models.ImageField(upload_to='users/', verbose_name='avatar',
                               **NULLABLE)
    phone = models.CharField(max_length=150, verbose_name='phone', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='country',
                               **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
