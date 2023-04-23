from django.shortcuts import render
from django.views import generic
from rest_framework import generics, status
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer


def index(request):
    """View function for the home page of the site."""

    num_books = Book.objects.count()

    context = {
        "num_books": num_books,
    }

    return render(request, "books/index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book
