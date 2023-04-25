from django.urls import path

from borrowing.views import (
    BorrowingList,
    BorrowingDetail,
    ReturnBorrowingView,
    CreateBorrowingView,
)

urlpatterns = [
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
]

app_name = "borrowing"
