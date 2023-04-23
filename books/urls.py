from django.urls import path
from books.views import (
    index,
    BookList,
    BookDetail
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
]

app_name = "books"
