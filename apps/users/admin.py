"""
Users 앱 Admin 설정
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    사용자 관리자 설정
    """

    list_display = (
        "email",
        "username",
        "nickname",
        "is_verified",
        "is_active",
        "created_at",
    )
    list_filter = ("is_verified", "is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email", "username", "nickname")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "개인정보",
            {"fields": ("username", "nickname", "phone_number", "birth_date")},
        ),
        ("프로필", {"fields": ("profile_image", "bio")}),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("중요한 일자", {"fields": ("last_login", "date_joined", "last_login_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    사용자 프로필 관리자 설정
    """

    list_display = ("user", "company", "job_title", "is_public", "created_at")
    list_filter = (
        "is_public",
        "email_notifications",
        "push_notifications",
        "created_at",
    )
    search_fields = ("user__email", "user__username", "company", "job_title")
    ordering = ("-created_at",)

    fieldsets = (
        ("기본 정보", {"fields": ("user",)}),
        ("추가 정보", {"fields": ("website", "location", "company", "job_title")}),
        (
            "설정",
            {"fields": ("is_public", "email_notifications", "push_notifications")},
        ),
    )
