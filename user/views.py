from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == "create":
            return []
        return super().get_permissions()


@api_view(["POST"])
def register_user(request):
    """
    Endpoint: /register/
    Method: POST
    Expected Input (Request Body):
    {
        "username": string,
        "email": string,
        "password": string
    }
    Expected Output (Response):
    {
        "message": string,
        "user": {
            "id": integer,
            "username": string,
            "email": string,
            ...
        },
        "access_token": string,
        "refresh_token": string
    }
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.create_user(username=username, email=email, password=password)

    serializer = UserSerializer(user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response_data = {
        "message": "User registered successfully",
        "user": serializer.data,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return Response(response_data, status=status.HTTP_201_CREATED)
