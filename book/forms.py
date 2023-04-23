from django import forms

from book import models


class Payment(models.Model):
    def __init__(self):
        self.money_to_pay = None

    def calculate_money_to_pay(self):
        borrow_date = self.borrowing_id.borrow_date
        expected_return_date = self.borrowing_id.expected_return_date

        days_borrowed = (expected_return_date - borrow_date).days

        total_price = days_borrowed * self.borrowing_id.book_id.daily_fee

        self.money_to_pay = total_price

        self.save()

        return total_price
