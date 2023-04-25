from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import (
    UserCreateView,
    UserRetrieveView,
    UserUpdateView,
    UserDeleteView
)

urlpatterns = [
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

app_name = "user"
