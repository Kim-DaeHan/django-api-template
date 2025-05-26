"""
Posts 앱 Admin 설정
"""

from django.contrib import admin

from .models import Category, Comment, Post, PostLike, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    게시글 관리자 설정
    """

    list_display = (
        "title",
        "author",
        "status",
        "view_count",
        "like_count",
        "created_at",
    )
    list_filter = ("status", "category", "created_at", "published_at")
    search_fields = ("title", "content", "author__email", "author__username")
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)

    fieldsets = (
        ("기본 정보", {"fields": ("title", "content", "summary", "author")}),
        ("분류", {"fields": ("category", "tags")}),
        ("상태", {"fields": ("status", "featured_image")}),
        ("통계", {"fields": ("view_count", "like_count", "comment_count")}),
        ("일시", {"fields": ("published_at",)}),
    )

    readonly_fields = ("view_count", "like_count", "comment_count")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    카테고리 관리자 설정
    """

    list_display = ("name", "parent", "order", "is_active", "created_at")
    list_filter = ("is_active", "parent", "created_at")
    search_fields = ("name", "description")
    ordering = ("order", "name")

    fieldsets = (
        ("기본 정보", {"fields": ("name", "slug", "description", "color")}),
        ("계층 구조", {"fields": ("parent", "order")}),
        ("상태", {"fields": ("is_active",)}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    태그 관리자 설정
    """

    list_display = ("name", "usage_count", "created_at")
    search_fields = ("name", "description")
    ordering = ("-usage_count", "name")
    readonly_fields = ("usage_count",)

    fieldsets = (
        ("기본 정보", {"fields": ("name", "slug", "description")}),
        ("통계", {"fields": ("usage_count",)}),
    )


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """
    게시글 좋아요 관리자 설정
    """

    list_display = ("post", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__title", "user__email", "user__username")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    댓글 관리자 설정
    """

    list_display = (
        "post",
        "author",
        "content_preview",
        "parent",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("content", "author__email", "author__username", "post__title")
    ordering = ("-created_at",)

    def content_preview(self, obj):
        """댓글 내용 미리보기"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "내용 미리보기"
