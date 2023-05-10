from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework.permissions import IsAuthenticated
# Register API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import *
from .serializers import *


@api_view(["POST"])
def signup(request):
    if "username" not in request.data or "password" not in request.data or "password2" not in request.data:
        return Response({"message": "fill all fields"})
    name = request.data["username"]
    password = request.data["password"]
    password2 = request.data["password2"]

    if password != password2:
        return Response({"message": "passwords not match"})

    user = User.objects.create(
        username=name,
    )
    user.set_password(password)
    user.save()
    return Response({"message": "user created"})


class Logoutview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        OutstandingToken.objects.filter(user=request.user).delete()

        return Response({"message": 'user logout'})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

class UserCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        profile = Profile.objects.first()  # یا هر دیگر روشی برای گرفتن پروفایل
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = Profile.objects.first()  # یا هر دیگر روشی برای گرفتن پروفایل
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
