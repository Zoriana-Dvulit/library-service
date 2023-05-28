from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == "create":
            return []
        return super().get_permissions()

    @action(methods=["POST"], detail=False)
    def register_user(self, request):
        """
        Endpoint: /user/register/
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
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "message": "User registered successfully",
                "user": UserSerializer(user).data,
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)