"""
공통 모델
모든 앱에서 공통으로 사용하는 추상 모델들
"""

from django.db import models


class TimeStampedModel(models.Model):
    """
    생성일시, 수정일시를 포함하는 추상 모델
    """

    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정일시", auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    소프트 삭제를 지원하는 추상 모델
    """

    is_deleted = models.BooleanField("삭제 여부", default=False)
    deleted_at = models.DateTimeField("삭제일시", null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """소프트 삭제 실행"""
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """삭제 복원"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """
    기본 모델 (타임스탬프 + 소프트 삭제)
    """

    class Meta:
        abstract = True
