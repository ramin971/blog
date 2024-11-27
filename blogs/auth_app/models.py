# from django.db import models
from django.contrib.auth.models import AbstractUser

# require for custom-user ------------------
class User(AbstractUser):
    pass
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(unique=True)