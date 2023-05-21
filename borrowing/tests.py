from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from books.models import Book
from borrowing.models import Borrowing
from borrowing.views import BorrowingViewSet


class BorrowingModelTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=1.99
        )
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=timezone.now().date()
        )

    def test_borrowing_model_str(self):
        expected_str = f"Borrowing of {self.book.id} by {self.user.id} (Expected return date: {self.borrowing.expected_return_date})"
        self.assertEqual(str(self.borrowing), expected_str)


class BorrowingViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BorrowingViewSet.as_view({"get": "list"})
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=1.99
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=timezone.now().date()
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_borrowing_list_authenticated(self):
        request = self.factory.get(reverse("borrowing-list"))
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrowing_list_unauthenticated(self):
        request = self.factory.get(reverse("borrowing-list"))
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_borrowing_create(self):
        data = {
            "book": self.book.id,
            "expected_return_date": timezone.now().date()
        }
        response = self.client.post(reverse("borrowing-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_borrowing_destroy(self):
        borrowing_id = self.borrowing.id
        response = self.client.delete(reverse("borrowing-detail", args=[borrowing_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Borrowing.objects.count(), 0)
