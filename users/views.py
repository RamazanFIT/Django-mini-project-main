from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission

from .serializers import UserSerializer

User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    """
    Allows Admin to list users and handle user registration.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            # Only Admin can view user list
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows user detail retrieval or update by Admin or the user themself.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]  # Custom permission defined below
        return super().get_permissions()


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only the user or an admin to edit user data.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
