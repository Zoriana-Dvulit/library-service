from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from books.models import Book
from books.serializers import BookSerializer
from books.views import BookViewSet

User = get_user_model()


class BookModelTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=1.99
        )

    def test_book_model_str(self):
        self.assertEqual(str(self.book), "Test Book")


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BookViewSet.as_view({"get": "list"})
        self.user = User.objects.create_user(username="testuser1", password="testpassword1")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=1.99
        )

    def test_book_list_authenticated(self):
        request = self.factory.get("/books/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_book_list_unauthenticated(self):
        request = self.factory.get("/books/")
        response = self.view(request)
        self.assertEqual(response.status_code, 401)

    def test_book_list_data(self):
        request = self.factory.get("/books/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = BookSerializer(instance=Book.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
