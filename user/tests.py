from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from user.views import UserViewSet
from user.serializers import UserSerializer

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view(
            {"get": "list", "post": "create", "patch": "partial_update", "delete": "destroy"})
        self.client = APIClient()

    def test_list_users(self):
        User.objects.create_user(username="user1", email="user1@example.com")
        User.objects.create_user(username="user2", email="user2@example.com")

        request = self.factory.get(reverse("user-list"))

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_user(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}

        request = self.factory.post(reverse("user-list"), data=data)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_update_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com")

        data = {"email": "updated@example.com"}

        request = self.factory.patch(reverse("user-detail", args=[user.pk]), data=data)
        request.user = user

        response = self.view(request, pk=user.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")

    def test_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com")

        request = self.factory.delete(reverse("user-detail", args=[user.pk]))
        request.user = user

        response = self.view(request, pk=user.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(pk=user.pk).exists())
