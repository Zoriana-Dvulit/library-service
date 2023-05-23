from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser and "user_id" in self.request.query_params:
            user_id = self.request.query_params["user_id"]
            queryset = Borrowing.objects.filter(user__id=user_id)
        elif self.request.user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user=self.request.user)

        if "is_active" in self.request.query_params:
            is_active = self.request.query_params["is_active"]
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.exclude(actual_return_date__isnull=True)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return HttpResponse(status=201, headers=headers)

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        return borrowing

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book = instance.book
        book.inventory += 1
        book.save()
        return super().destroy(request, *args, **kwargs)


class ReturnBorrowingView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request, borrowing_id):
        borrowing = get_object_or_404(Borrowing, pk=borrowing_id)

        if borrowing.actual_return_date is not None:
            return HttpResponseBadRequest
