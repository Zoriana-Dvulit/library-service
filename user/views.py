from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
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
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.create_user(username=username, email=email, password=password)

    user.set_password(password)
    user.save()

    serializer = UserSerializer(user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({
        "message": "User registered successfully",
        "user": serializer.data,
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    response["Authorization"] = f"Bearer {access_token}"

    return response
