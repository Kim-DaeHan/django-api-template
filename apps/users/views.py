"""
Users 앱 뷰
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.utils import create_response

from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자 ViewSet
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        권한 설정
        """
        if self.action in ["create"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        현재 사용자 정보 조회
        """
        serializer = self.get_serializer(request.user)
        return create_response(
            success=True,
            message="사용자 정보를 성공적으로 조회했습니다.",
            data=serializer.data,
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    사용자 프로필 조회/수정 뷰
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        현재 사용자의 프로필 반환
        """
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class CurrentUserView(generics.RetrieveAPIView):
    """
    현재 사용자 정보 조회 뷰
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        현재 사용자 반환
        """
        return self.request.user
