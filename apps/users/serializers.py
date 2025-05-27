"""
Users 앱 시리얼라이저
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    사용자 시리얼라이저
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "nickname",
            "phone_number",
            "birth_date",
            "bio",
            "profile_image",
            "is_verified",
            "is_active",
            "created_at",
            "updated_at",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ["id", "created_at", "updated_at", "is_verified"]

    def create(self, validated_data):
        """
        사용자 생성
        """
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    사용자 프로필 시리얼라이저
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "website",
            "location",
            "company",
            "job_title",
            "is_public",
            "email_notifications",
            "push_notifications",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
