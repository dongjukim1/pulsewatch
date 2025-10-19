# PulseWatch NHK Quickstart

NHK RSS 피드를 수집해 토큰화하고 WebSocket으로 전달하는 MVP 프로젝트입니다. 아래 순서를 따라 빠르게 실행해 보세요.

## 1. 환경 변수 준비

```bash
cp .env.example .env
```

필요에 따라 `.env` 파일에서 `NHK_FEEDS` 등 환경 변수를 수정합니다.

## 2. Docker Compose 실행 (API + Worker + Redis)

```bash
cd infra
docker compose up --build
```

## 3. 서비스 확인

- **Health Check**
  ```bash
  curl http://localhost:8000/healthz
  ```
- **실시간 스트림 테스트**
  - WebSocket 엔드포인트: `ws://localhost:8000/ws/stream`
  - 루트 디렉터리에 있는 `index.html`을 브라우저에서 열어 간단하게 메시지를 확인할 수 있습니다.

## 4. 로컬 개발 (Docker 없이)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload
celery -A worker.celery_app:celery worker --loglevel=INFO --concurrency=4
```

## 5. 다음 단계 (To-Do)

- 토크나이저를 Janome 또는 SudachiPy로 교체
- 상위 키워드 집계 API: 최근 5분 대비 이전 5분 변화율 계산
- WebSocket을 통한 Top 카드 실시간 푸시
- (2단계) Elasticsearch/Kibana 연동
