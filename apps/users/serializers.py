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
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

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
            "bio",
            "birth_date",
            "phone_number",
            "avatar",
            "website",
            "location",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
