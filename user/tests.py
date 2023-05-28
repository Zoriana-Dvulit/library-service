from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from user.serializers import UserSerializer
from user.views import UserViewSet

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser2", password="testpassword2")
        self.view = UserViewSet.as_view(
            {"get": "list", "post": "create", "patch": "partial_update", "delete": "destroy"})
        self.client = APIClient()

    def test_list_users(self):
        User.objects.create_user(username="user1", email="user1@example.com")
        User.objects.create_user(username="user2", email="user2@example.com")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("user:user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_user(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}

        request = self.factory.post(reverse("user:user-list"), data=data)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_update_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com")
        data = {"email": "updated@example.com"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse("user:user-detail", args=[user.pk]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")

    def test_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com")
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("user:user-detail", args=[user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(pk=user.pk).exists())
