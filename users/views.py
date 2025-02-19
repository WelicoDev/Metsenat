from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, LoginSerializer, ChangePasswordSerializer, ProfileSerializer,\
                          ProfileEditSerializer, LogoutSerializer)

User = get_user_model()


# SignUp View
class RegisterView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()  # Create User
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


# SignIn View
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Username or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Password View
class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password successfully updated."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View Profile View
class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


# Edit Profile View
class ProfileEditView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileEditSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Edit User Profile
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Token test

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()  # Token blocklist
            return Response({"detail": "Successful logout."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)