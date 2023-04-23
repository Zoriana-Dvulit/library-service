from django.contrib import admin

from .models import (
    Book,
    Customer,
    Borrowing,
    Payment,
)

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Borrowing)
admin.site.register(Payment)
