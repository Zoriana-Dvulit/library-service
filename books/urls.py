from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from books.views import (
    index,
    BookList,
    BookDetail, BorrowingList, BorrowingDetail, ReturnBorrowingView, CreateBorrowingView, UserCreateView,
    UserRetrieveView, UserUpdateView, UserDeleteView
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
        name="create_borrowing"
    ),
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "api/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify"
    ),
    path(
        "users/",
        UserCreateView.as_view(),
        name="user-create"
    ),
    path(
        "users/<int:pk>/",
        UserRetrieveView.as_view(),
        name="user-retrieve"
    ),
    path(
        "users/<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user-update"
    ),
    path(
        "users/<int:pk>/delete/",
        UserDeleteView.as_view(),
        name="user-delete"
    ),
]

app_name = "books"
