"""
Posts 앱 URL 설정
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "posts"

router = DefaultRouter()
router.register(r"", views.PostViewSet, basename="post")
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"tags", views.TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:post_id>/like/", views.PostLikeView.as_view(), name="post-like"),
    path(
        "<int:post_id>/comments/",
        views.CommentListCreateView.as_view(),
        name="post-comments",
    ),
    path(
        "comments/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment-detail",
    ),
]
