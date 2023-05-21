from django.conf import settings
from django.db import models

from books.models import Book


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
        return f"Payment for {self.type} ({self.status}) of {self.borrowing_id} by user {self.borrowing_id.user_id} for {self.money_to_pay}"

    def calculate_money_to_pay(self):
        borrow_date = self.borrowing_id.borrow_date
        expected_return_date = self.borrowing_id.expected_return_date

        days_borrowed = (expected_return_date - borrow_date).days

        total_price = days_borrowed * self.borrowing_id.book_id.daily_fee

        self.money_to_pay = total_price

        self.save()

        return total_price
