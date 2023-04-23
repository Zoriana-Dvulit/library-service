from django.conf import settings
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


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(expected_return_date__gte=models.F("borrow_date")),
                                   name="expected_return_date_gte_borrow_date"),
            models.CheckConstraint(check=models.Q(actual_return_date__gte=models.F("borrow_date")),
                                   name="actual_return_date_gte_borrow_date"),
            models.CheckConstraint(check=models.Q(actual_return_date__lte=models.F("expected_return_date")),
                                   name="actual_return_date_lte_expected_return_date"),
        ]

    def __str__(self):
        return f"Borrowing of {self.book_id} by {self.user_id} (Expected return date: {self.expected_return_date})"


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    api_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Payment for {self.type} ({self.status}) of {self.borrowing_id} by user {self.borrowing_id.user_id} for {self.money_to_pay} $USD"
