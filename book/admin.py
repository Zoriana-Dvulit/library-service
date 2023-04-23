from django.contrib import admin

from .models import (
    Book,
    User,
    Borrowing,
    Payment,
)

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Borrowing)
admin.site.register(Payment)
