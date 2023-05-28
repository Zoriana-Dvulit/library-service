from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=50, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.title
