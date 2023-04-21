from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    HARD = "H"
    SOFT = "S"
    COVER_CHOICES = [
        (HARD, "Hardcover"),
        (SOFT, "Softcover"),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=1, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Payment(models.Model):
    PENDING = 'P'
    PAID = 'A'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]
    PAYMENT = 'P'
    FINE = 'F'
    TYPE_CHOICES = [
        (PAYMENT, 'Payment'),
        (FINE, 'Fine'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    payment_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    payment_session_url = models.URLField(null=True, blank=True)
    payment_session_id = models.CharField(max_length=255, null=True, blank=True)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2, default=0)



class TelegramNotification(models.Model):
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    message = models.TextField()


class Payment(models.Model):
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Borrowing.STATUS_CHOICES, default=Borrowing.PENDING)
