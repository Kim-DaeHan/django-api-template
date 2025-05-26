"""
사용자 관리 모델
Toss 스타일의 네이밍 컨벤션을 따름
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    커스텀 사용자 모델
    """

    # 기본 필드 확장
    email = models.EmailField("이메일", unique=True)
    phone_number = models.CharField("전화번호", max_length=20, blank=True)
    birth_date = models.DateField("생년월일", null=True, blank=True)

    # 프로필 정보
    nickname = models.CharField("닉네임", max_length=50, blank=True)
    profile_image = models.ImageField(
        "프로필 이미지", upload_to="profiles/", blank=True
    )
    bio = models.TextField("자기소개", max_length=500, blank=True)

    # 상태 관리
    is_verified = models.BooleanField("인증 여부", default=False)
    is_active = models.BooleanField("활성 상태", default=True)

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)
    last_login_at = models.DateTimeField("마지막 로그인", null=True, blank=True)

    # 이메일을 username으로 사용
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.nickname or self.username})"

    @property
    def display_name(self):
        """표시용 이름 반환"""
        return self.nickname or self.username

    def update_last_login(self):
        """마지막 로그인 시간 업데이트"""
        self.last_login_at = timezone.now()
        self.save(update_fields=["last_login_at"])


class UserProfile(models.Model):
    """
    사용자 추가 프로필 정보
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="사용자"
    )

    # 추가 정보
    website = models.URLField("웹사이트", blank=True)
    location = models.CharField("위치", max_length=100, blank=True)
    company = models.CharField("회사", max_length=100, blank=True)
    job_title = models.CharField("직책", max_length=100, blank=True)

    # 설정
    is_public = models.BooleanField("공개 프로필", default=True)
    email_notifications = models.BooleanField("이메일 알림", default=True)
    push_notifications = models.BooleanField("푸시 알림", default=True)

    # 타임스탬프
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필들"

    def __str__(self):
        return f"{self.user.email}의 프로필"
