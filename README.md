# PyScraper

## 프로젝트 소개

특정 온라인 쇼핑몰의 상품 가격을 자동으로 수집하고, 간단한 형태로 제공하는 프로토타입입니다.
펫 관련 상품의 가격 변동을 추적하고, 가격 비교를 통해 합리적인 구매 결정을 돕는 것을 목표로 합니다.

## 주요 기능

- **데이터 수집**: `httpx`와 `BeautifulSoup`을 사용한 비동기 웹 스크래핑
- **주기적 실행**: `Celery`를 활용한 정기적 또는 수동 수집
- **데이터 저장**: `SQLite` 데이터베이스에 상품 정보 저장
- **CLI**: `argparse`를 이용한 커맨드 라인 인터페이스 제공

## 기술 스택

- **언어**: Python 3.12
- **데이터베이스**: SQLAlchemy, SQLite
- **스크래핑**: BeautifulSoup, httpx
- **데이터 모델링**: Pydantic
- **비동기 작업**: Celery, Celery Beat, Redis
- **패키지 관리**: Poetry

## 설치 및 실행

1. **의존성 설치**

```shell
poetry install
```

2. **Celery 실행**

Celery 워커와 비트를 각각 다른 터미널에서 실행합니다.

```shell
# Celery 워커 실행
celery -A app.config.celery worker --loglevel=INFO

# Celery 비트 실행
celery -A app.config.celery beat --loglevel=INFO
```

3. **데이터베이스 생성**

최초 실행 시 `main.py`를 실행하여 데이터베이스와 테이블을 생성합니다.

```shell
python main.py
```

## TODO

- [ ] Docker Compose를 이용한 간편한 실행 환경 구성
- [ ] Celery 작업 결과 추적 및 관리 기능 추가
- [ ] 테스트 코드 작성