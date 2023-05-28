from django.contrib import admin

from books.models import Book
from borrowing.models import Borrowing, Payment
from user.models import Customer

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Borrowing)
admin.site.register(Payment)
