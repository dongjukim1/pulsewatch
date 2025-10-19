# PulseWatch NHK — Quickstart


## 1) .env 만들기
cp .env.example .env
# 필요 시 NHK_FEEDS 수정


## 2) Docker Compose (redis + api + worker)
cd infra
docker compose up --build


## 3) 확인
# 1) 헬스체크
curl http://localhost:8000/healthz


# 2) 실시간 스트림 보기 (브라우저)
# ws://localhost:8000/ws/stream
# Simple 방법: 이 URL을 테스트용으로 여는 작은 HTML을 만드세요.


## 4) 로컬 개발(도커 없이)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload
celery -A worker.celery_app:celery worker --loglevel=INFO --concurrency=4


## 5) 다음 단계(To‑Do)
- 토큰화: Janome/SudachiPy로 교체
- 상위 키워드 집계 API: 최근 5분 vs 이전 5분 변화율 계산
- WebSocket으로 Top 카드 push
- (2단계) Elasticsearch/Kibana 연동