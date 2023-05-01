from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


# Create your views here.

class BorrowingList(generics.ListCreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | ~IsAdminUser)]

    def get_queryset(self):
        if self.request.user.is_superuser and "user_id" in self.request.query_params:
            user_id = self.request.query_params["user_id"]
            queryset = Borrowing.objects.filter(borrower__id=user_id)
        elif self.request.user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(borrower=self.request.user)

        if "is_active" in self.request.query_params:
            is_active = self.request.query_params["is_active"]
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.exclude(actual_return_date__isnull=True)

        return queryset


class BorrowingDetail(generics.RetrieveAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Borrowing.objects.all()


class CreateBorrowingView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]


class ReturnBorrowingView(View):
    def post(self, request, borrowing_id):
        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        if borrowing.actual_return_date is not None:
            return HttpResponseBadRequest("Borrowing has already been returned")

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return HttpResponse("Borrowing has been returned successfully")
