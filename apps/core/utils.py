"""
공통 유틸리티 함수들
Toss 스타일의 네이밍 컨벤션을 따름
"""

import hashlib
import uuid
from typing import Any, Dict, Optional

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone


def generate_unique_id() -> str:
    """
    고유 ID 생성
    """
    return str(uuid.uuid4())


def generate_hash(text: str) -> str:
    """
    텍스트 해시 생성
    """
    return hashlib.sha256(text.encode()).hexdigest()


def create_response(
    success: bool = True,
    message: str = "",
    data: Optional[Dict[str, Any]] = None,
    status_code: int = 200,
) -> JsonResponse:
    """
    표준 API 응답 생성
    """
    response_data = {
        "success": success,
        "message": message,
        "timestamp": timezone.now().isoformat(),
    }

    if data is not None:
        response_data["data"] = data

    return JsonResponse(response_data, status=status_code)


def create_error_response(
    message: str, error_code: Optional[str] = None, status_code: int = 400
) -> JsonResponse:
    """
    에러 응답 생성
    """
    response_data = {
        "success": False,
        "message": message,
        "timestamp": timezone.now().isoformat(),
    }

    if error_code:
        response_data["error_code"] = error_code

    return JsonResponse(response_data, status=status_code)


def paginate_queryset(queryset, page_number: int, page_size: int = 20):
    """
    쿼리셋 페이지네이션
    """
    paginator = Paginator(queryset, page_size)
    page = paginator.get_page(page_number)

    return {
        "items": page.object_list,
        "pagination": {
            "current_page": page.number,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "page_size": page_size,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
        },
    }


def validate_email(email: str) -> bool:
    """
    이메일 유효성 검사
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone_number(phone: str) -> bool:
    """
    전화번호 유효성 검사 (한국 형식)
    """
    import re

    pattern = r"^01[0-9]-?[0-9]{4}-?[0-9]{4}$"
    return re.match(pattern, phone) is not None


def format_phone_number(phone: str) -> str:
    """
    전화번호 포맷팅
    """
    # 숫자만 추출
    digits = "".join(filter(str.isdigit, phone))

    if len(digits) == 11 and digits.startswith("01"):
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"

    return phone


def get_client_ip(request) -> str:
    """
    클라이언트 IP 주소 추출
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    텍스트 자르기
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix
