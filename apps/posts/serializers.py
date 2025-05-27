"""
Posts 앱 시리얼라이저
"""

from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Category, Comment, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    """
    카테고리 시리얼라이저
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TagSerializer(serializers.ModelSerializer):
    """
    태그 시리얼라이저
    """

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    """
    게시글 시리얼라이저
    """

    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "category",
            "category_id",
            "tags",
            "tag_ids",
            "status",
            "featured_image",
            "like_count",
            "comment_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        게시글 생성
        """
        tag_ids = validated_data.pop("tag_ids", [])
        post = Post.objects.create(**validated_data)

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)

        return post

    def update(self, instance, validated_data):
        """
        게시글 수정
        """
        tag_ids = validated_data.pop("tag_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    """
    댓글 시리얼라이저
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "post",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "post", "created_at", "updated_at"]
