"""
Users 앱 URL 설정
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter()
router.register(r"", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("me/", views.CurrentUserView.as_view(), name="current-user"),
]
