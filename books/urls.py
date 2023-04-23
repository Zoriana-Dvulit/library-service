from django.urls import path

from books.models import Borrowing
from books.views import (
    index,
    BookList,
    BookDetail, BorrowingList, BorrowingDetail
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "books/",
        BookList.as_view(),
        name="book-list",
    ),
    path(
        "books/<int:pk>/",
        BookDetail.as_view(),
        name="book-detail",
    ),
    path(
        "borrowings/",
        BorrowingList.as_view(),
        name="borrowing-list"
    ),
    path(
        "borrowings/<int:pk>/",
        BorrowingDetail.as_view(),
        name="borrowing-detail"
    ),
]

app_name = "books"
