from django.contrib.auth.models import AbstractUser
from django.db import models
from colossus.apps.accounts.managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
from typing import List


class User(AbstractUser):
    """
    This is the class to define the user model.
    """
    timezone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[int] = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        """
        This is the meta class of class User used to define the table name in the database.
        """
        db_table = 'auth_user'
