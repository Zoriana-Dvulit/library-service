from django.urls import path

from books.models import Borrowing
from books.views import (
    index,
    BookList,
    BookDetail, BorrowingList, BorrowingDetail, ReturnBorrowingView, CreateBorrowingView
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
    path(
        "borrowings/<int:borrowing_id>/return/",
        ReturnBorrowingView.as_view(),
        name="return-borrowing"
    ),
    path(
        "borrowings/create/",
        CreateBorrowingView.as_view(),
        name="create_borrowing"),
]

app_name = "books"
