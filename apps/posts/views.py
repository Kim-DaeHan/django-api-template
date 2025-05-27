"""
Posts 앱 뷰
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.core.utils import create_response

from .models import Category, Comment, Post, PostLike, Tag
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
    TagSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """
    게시글 ViewSet
    """

    queryset = Post.objects.select_related("author", "category").prefetch_related(
        "tags"
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        게시글 생성 시 작성자 설정
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        게시글 좋아요/취소
        """
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            message = "좋아요를 취소했습니다."
            is_liked = False
        else:
            message = "좋아요를 눌렀습니다."
            is_liked = True

        return create_response(
            success=True,
            message=message,
            data={"is_liked": is_liked, "like_count": post.like_count},
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """
    카테고리 ViewSet
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    태그 ViewSet
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostLikeView(generics.CreateAPIView):
    """
    게시글 좋아요 뷰
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        게시글 좋아요/취소
        """
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            message = "좋아요를 취소했습니다."
            is_liked = False
        else:
            message = "좋아요를 눌렀습니다."
            is_liked = True

        return create_response(
            success=True,
            message=message,
            data={"is_liked": is_liked, "like_count": post.like_count},
        )


class CommentListCreateView(generics.ListCreateAPIView):
    """
    댓글 목록 조회/생성 뷰
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        특정 게시글의 댓글들만 반환
        """
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).select_related("author")

    def perform_create(self, serializer):
        """
        댓글 생성 시 작성자와 게시글 설정
        """
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    댓글 상세 조회/수정/삭제 뷰
    """

    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "comment_id"

    def get_permissions(self):
        """
        권한 설정 - 작성자만 수정/삭제 가능
        """
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
