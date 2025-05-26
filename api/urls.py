"""
API 메인 URL 설정
"""

from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.core.utils import create_response


@api_view(["GET"])
def api_root(request):
    """
    API 루트 엔드포인트
    """
    data = {
        "message": "Social API v1",
        "endpoints": {
            "users": "/api/v1/users/",
            "posts": "/api/v1/posts/",
            "admin": "/admin/",
        },
    }
    return Response(data)


urlpatterns = [
    path("", api_root, name="api-root"),
]
