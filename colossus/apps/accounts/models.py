from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    This is the class to define the user model.
    """
    timezone = models.CharField(max_length=50, blank=True)

    class Meta:
        """
        This is the meta class of class User used to define the table name in the database.
        """
        db_table = 'auth_user'
