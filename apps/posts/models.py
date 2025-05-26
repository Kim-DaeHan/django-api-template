"""
게시글 관리 모델
Toss 스타일의 네이밍 컨벤션을 따름
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class PostStatus(models.TextChoices):
    """게시글 상태"""

    DRAFT = "draft", "임시저장"
    PUBLISHED = "published", "게시됨"
    ARCHIVED = "archived", "보관됨"
    DELETED = "deleted", "삭제됨"


class Post(models.Model):
    """
    게시글 모델
    """

    # 기본 정보
    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    summary = models.TextField("요약", max_length=300, blank=True)

    # 관계
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="작성자",
    )

    # 상태 관리
    status = models.CharField(
        "상태", max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT
    )

    # 메타데이터
    view_count = models.PositiveIntegerField("조회수", default=0)
    like_count = models.PositiveIntegerField("좋아요 수", default=0)
    comment_count = models.PositiveIntegerField("댓글 수", default=0)

    # 이미지
    featured_image = models.ImageField("대표 이미지", upload_to="posts/", blank=True)

    # 태그 및 카테고리
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="태그")
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="카테고리",
    )

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)
    published_at = models.DateTimeField("게시일시", null=True, blank=True)

    class Meta:
        db_table = "posts"
        verbose_name = "게시글"
        verbose_name_plural = "게시글들"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["author", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.author.display_name}"

    def publish(self):
        """게시글 발행"""
        self.status = PostStatus.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=["status", "published_at"])

    def archive(self):
        """게시글 보관"""
        self.status = PostStatus.ARCHIVED
        self.save(update_fields=["status"])

    def increment_view_count(self):
        """조회수 증가"""
        self.view_count += 1
        self.save(update_fields=["view_count"])

    @property
    def is_published(self):
        """게시 여부 확인"""
        return self.status == PostStatus.PUBLISHED


class Category(models.Model):
    """
    게시글 카테고리
    """

    name = models.CharField("카테고리명", max_length=50, unique=True)
    slug = models.SlugField("슬러그", unique=True)
    description = models.TextField("설명", blank=True)
    color = models.CharField("색상", max_length=7, default="#000000")

    # 계층 구조
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="상위 카테고리",
    )

    # 정렬 순서
    order = models.PositiveIntegerField("정렬 순서", default=0)

    # 상태
    is_active = models.BooleanField("활성 상태", default=True)

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

    class Meta:
        db_table = "categories"
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리들"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    게시글 태그
    """

    name = models.CharField("태그명", max_length=50, unique=True)
    slug = models.SlugField("슬러그", unique=True)
    description = models.TextField("설명", blank=True)

    # 사용 횟수
    usage_count = models.PositiveIntegerField("사용 횟수", default=0)

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

    class Meta:
        db_table = "tags"
        verbose_name = "태그"
        verbose_name_plural = "태그들"
        ordering = ["-usage_count", "name"]

    def __str__(self):
        return self.name


class PostLike(models.Model):
    """
    게시글 좋아요
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", verbose_name="게시글"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_likes",
        verbose_name="사용자",
    )

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)

    class Meta:
        db_table = "post_likes"
        verbose_name = "게시글 좋아요"
        verbose_name_plural = "게시글 좋아요들"
        unique_together = ["post", "user"]

    def __str__(self):
        return f"{self.user.display_name}이 {self.post.title}을 좋아함"


class Comment(models.Model):
    """
    댓글 모델
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="게시글"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="작성자",
    )

    # 댓글 내용
    content = models.TextField("내용")

    # 대댓글 지원
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="상위 댓글",
    )

    # 상태
    is_active = models.BooleanField("활성 상태", default=True)

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

    class Meta:
        db_table = "comments"
        verbose_name = "댓글"
        verbose_name_plural = "댓글들"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.display_name}의 댓글: {self.content[:50]}"
