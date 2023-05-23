from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from books.models import Book
from borrowing.models import Borrowing
from borrowing.views import BorrowingViewSet
from user.models import Customer as User


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
        self.view_list = BorrowingViewSet.as_view({"get": "list", "post": "create"})
        self.view_detail = BorrowingViewSet.as_view({"get": "retrieve", "delete": "destroy"})
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
        request = self.factory.get(reverse("borrowing:borrowing-list"))
        force_authenticate(request, user=self.user)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_borrowing_create(self):
        data = {
            "book": self.book.id,
            "expected_return_date": timezone.now().date()
        }
        request = self.factory.post(reverse("borrowing:borrowing-list"), data, format="json")
        force_authenticate(request, user=self.user)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

    def test_borrowing_destroy(self):
        borrowing_id = self.borrowing.id
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/borrowing/{borrowing_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Borrowing.objects.count(), 0)
