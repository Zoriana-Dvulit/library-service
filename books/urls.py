from django.urls import path
from books.views import (
    index,
    BookListView,
    BookDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "books/",
        BookListView.as_view(),
        name="books-list",
    ),
    path(
        "books/<int:pk>/",
        BookDetailView.as_view(),
        name="books_detail",
    ),
]

app_name = "books"
