from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book, Borrowing
from books.serializers import BookSerializer, BorrowingSerializer


def index(request):
    """View function for the home page of the site."""

    num_books = Book.objects.count()

    context = {
        "num_books": num_books,
    }

    return render(request, "books/index.html", context=context)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class BorrowingList(generics.ListCreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrowing.objects.filter(user_id=self.request.user)


class BorrowingDetail(generics.RetrieveAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Borrowing.objects.all()
