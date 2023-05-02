from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer


def sample_book(title="Sample Book", author="Sample Author", cover="Hard", inventory=10, daily_fee="10.00"):
    """Створити зразкову книгу"""
    return Book.objects.create(title=title, author=author, cover=cover, inventory=inventory, daily_fee=daily_fee)


class PublicBooksApiTests(TestCase):
    """Тести публічного доступу до API Книг"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Тест, що перевіряє, що логін є обов'язковим для доступу до книг"""
        url = reverse("books:book-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBooksApiTests(TestCase):
    """Тести приватного доступу до API Книг"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@test.com",
            password="testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        """Тест, що перевіряє отримання списку книг"""
        sample_book()
        sample_book()

        url = reverse("books:book-list")
        res = self.client.get(url)

        books = Book.objects.all().order_by("-id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_successful(self):
        """Тест, що перевіряє створення нової книги"""
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "Soft",
            "inventory": 5,
            "daily_fee": "8.50"
        }
        url = reverse("books:book-list")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data["id"])
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_create_book_invalid(self):
        """Тест, що перевіряє створення недійсної книги"""
        payload = {
            "title": "",
            "author": "New Author",
            "cover": "Soft",
            "inventory": 5,
            "daily_fee": "8.50"
        }
        url = reverse("books:book-list")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_book(self):
        """Тест, що перевіряє часткове оновлення книги"""
        book = sample_book()
        new_title = "New Title"

        payload = {"title": new_title}
        url = reverse("books:book-detail", args=[book.id])
        res = self.client.patch(url, payload)

        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, new_title)
