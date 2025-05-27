# Social API

Django REST Framework를 사용한 소셜 미디어 API 프로젝트입니다.

## 🏗️ 프로젝트 구조

```
social_api/
├── manage.py                 # Django 프로젝트 실행 파일
├── social_api/               # 프로젝트 설정
│   ├── settings/            # 환경별 설정
│   │   ├── base.py         # 공통 설정
│   │   ├── dev.py          # 개발 환경 설정
│   │   └── prod.py         # 프로덕션 환경 설정
│   ├── urls.py             # 프로젝트 URL 라우팅
│   ├── wsgi.py             # WSGI (배포용)
│   └── asgi.py             # ASGI (비동기 지원)
├── apps/                     # 앱 모듈
│   ├── users/               # 사용자 관리 앱
│   ├── posts/               # 게시글 관리 앱
│   └── core/                # 공통 기능
├── api/                      # REST API (DRF)
├── requirements/             # 의존성
│   ├── base.txt            # 공통 의존성
│   ├── dev.txt             # 개발용 의존성
│   └── prod.txt            # 프로덕션 의존성
└── static/                   # 정적 파일
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# Django 설정
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 데이터베이스 설정
DATABASE_URL=postgresql://hans:@localhost:5432/social_api_dev

# Redis 설정 (프로덕션용)
REDIS_URL=redis://127.0.0.1:6379/1

# Sentry 설정 (모니터링, 프로덕션용)
SENTRY_DSN=https://your-sentry-dsn-here
```

> **참고**: 위의 DATABASE_URL에서 `hans`는 현재 시스템 사용자명입니다. 본인의 사용자명으로 변경하세요.

### 3. 데이터베이스 설정

```bash
# PostgreSQL 데이터베이스 생성
createdb social_api_dev

# 마이그레이션 실행
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

### 4. 서버 실행

```bash
python manage.py runserver
```

## 📚 API 엔드포인트

### 사용자 관리

- `GET /api/v1/users/` - 사용자 목록
- `POST /api/v1/users/` - 사용자 생성
- `GET /api/v1/users/{id}/` - 사용자 상세
- `PUT /api/v1/users/{id}/` - 사용자 수정
- `DELETE /api/v1/users/{id}/` - 사용자 삭제
- `GET /api/v1/users/me/` - 현재 사용자 정보
- `GET /api/v1/users/profile/` - 사용자 프로필

### 게시글 관리

- `GET /api/v1/posts/` - 게시글 목록
- `POST /api/v1/posts/` - 게시글 생성
- `GET /api/v1/posts/{id}/` - 게시글 상세
- `PUT /api/v1/posts/{id}/` - 게시글 수정
- `DELETE /api/v1/posts/{id}/` - 게시글 삭제
- `POST /api/v1/posts/{id}/like/` - 게시글 좋아요
- `GET /api/v1/posts/{id}/comments/` - 댓글 목록
- `POST /api/v1/posts/{id}/comments/` - 댓글 생성

### 카테고리 & 태그

- `GET /api/v1/posts/categories/` - 카테고리 목록
- `GET /api/v1/posts/tags/` - 태그 목록

## 🛠️ 기술 스택

- **Backend**: Django 5.2.1, Django REST Framework 3.15.2
- **Database**: PostgreSQL
- **Authentication**: Django Session Authentication, Token Authentication
- **Code Style**: Toss 코드 컨벤션 적용

## 📋 주요 기능

### 사용자 관리

- 커스텀 사용자 모델 (이메일 기반 인증)
- 사용자 프로필 관리
- 인증 및 권한 관리

### 게시글 관리

- 게시글 CRUD
- 카테고리 및 태그 시스템
- 좋아요 기능
- 댓글 및 대댓글 시스템
- 게시글 상태 관리 (임시저장, 게시됨, 보관됨, 삭제됨)

### 공통 기능

- 페이지네이션
- 검색 및 필터링
- 소프트 삭제
- 타임스탬프 관리

## 🔧 개발 도구

```bash
# 코드 포맷팅
black .
isort .

# 린팅
flake8

# 테스트 실행
pytest
```

## 📝 환경별 설정

### 개발 환경

```bash
python manage.py runserver --settings=social_api.settings.dev
```

### 프로덕션 환경

```bash
python manage.py runserver --settings=social_api.settings.prod
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.
