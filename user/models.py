from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group", related_name="customers", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="customers", blank=True
    )

    def __str__(self):
        return self.username
