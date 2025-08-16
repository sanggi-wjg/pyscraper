# PyScraper

이 프로젝트는 거창한 비전도, 대단한 목적도 없습니다.
그저 요즘 핫하다는 “바이브 머시기 코딩”이 뭔가 싶어서,
호기심 반 심심함 반으로 만들어본 실험작입니다.

한마디로 말하자면, “나도 한번 해봤다 바이브 코딩” 프로젝트입니다.
해보았는데 얼추 그럴듯 하게 만들어는주지만 버그 있는 코드를 많이 만들고 결국 제가 다시 작성한 부분이 많았습니다.

## 작성이 잘 되는 부분:
- markdown 문서는 이 친구가 다 했습니다.
- 코드를 참고해서 만들어달라고 하면 잘 만들어줍니다.

## 작성이 잘 안되는 부분:
- Transactional 데코레이터 생성시 버그 투성인 코드를 생성 했습니다.
- 기존에 잘 작성된 코드고 수정하지 말라고 했는데 버그를 포함시켜 수정하는 현상이 있었습니다.

자세한 내용은 LOG.md 작성

## 1. 프로젝트 소개

**PyScraper**는 주요 온라인 펫 커머스 플랫폼의 상품 가격을 주기적으로 수집, 저장하고 조회할 수 있는 웹 스크레이핑 프로토타입입니다.

CLI를 통해 스크레이핑할 키워드를 등록하면, Celery 워커가 주기적으로 해당 키워드의 상품 정보를 수집하여 데이터베이스에 저장합니다. 사용자는 저장된 데이터를 바탕으로 상품의 가격 변동 이력을 추적하고, 구매 결정에 참고할 수 있습니다.

## 2. 주요 기능

- **주기적 데이터 수집**: `Celery Beat`를 사용하여 등록된 키워드에 대한 상품 정보를 매시간 자동으로 스크레이핑합니다.
- **스크레이핑**: `httpx`와 `BeautifulSoup4`를 활용하여 여러 상품 페이지를 효율적으로 처리합니다.
- **데이터베이스 관리**: `SQLAlchemy` ORM을 통해 수집된 데이터를 `SQLite` 데이터베이스에 저장하고 관리합니다.
- **CLI 제공**: `argparse`를 기반으로 키워드 등록, 데이터베이스 테이블 생성, 상품 가격 이력 조회 등 주요 기능을 실행할 수 있는 CLI를 제공합니다.
- **확장 가능한 구조**: `app/scraper/sites` 디렉토리에 신규 스크래퍼를 추가하여 손쉽게 지원 쇼핑몰을 확장할 수 있습니다.

## 3. 기술 스택

- **언어**: Python 3.12+
- **데이터베이스**: SQLAlchemy (ORM), SQLite
- **웹 스크레이핑**: httpx, BeautifulSoup4, fake-useragent
- **데이터 모델링**: Pydantic
- **비동기 작업**: Celery, Redis (Broker)
- **CLI**: argparse
- **패키지 관리**: Poetry
- **코드 스타일**: Black

## 4. 설치 및 실행

### 4.1. 사전 요구사항

- Python 3.12 이상
- Poetry
- Redis (Celery 메시지 브로커로 사용)

### 4.2. 설치

1. **프로젝트 클론**

```shell
git clone https://github.com/your-username/pyscraper.git
cd pyscraper
```

2. **의존성 설치**
   `poetry`를 사용하여 프로젝트 의존성을 설치합니다.

```shell
poetry install
```

### 4.3. 실행

1. **데이터베이스 테이블 생성**
   최초 실행 시, 다음 명령어로 `SQLite` 데이터베이스 파일과 테이블을 생성합니다.

```shell
poetry run python main.py --create-tables
```

2. **Celery 실행**
   데이터 수집을 위해 Celery 워커와 스케줄러(Beat)를 각각 다른 터미널에서 실행합니다. (백그라운드 실행 권장)

- **Celery 워커 실행**

 ```shell
 poetry run celery -A app.task.tasks worker --loglevel=INFO
 ```

- **Celery Beat 실행**

 ```shell
 poetry run celery -A app.task.tasks beat --loglevel=INFO
 ```

> **Note**: `app.config.celery` 대신 `app.task.tasks`를 entrypoint로 사용해야 Celery가 태스크를 올바르게 인식합니다.

## 5. 사용법

### 5.1. 스크레이핑 키워드 등록

Celery가 주기적으로 스크레이핑할 키워드를 등록합니다.

```shell
poetry run python main.py --create-keyword "강아지 간식"
```

### 5.2. 상품 가격 이력 조회

데이터베이스에 저장된 상품의 가격 변동 이력을 조회합니다.

```shell
poetry run python main.py --product-name "상품명 일부"
```

## 6. 향후 계획 (TODO)

- [ ] **FastAPI 서버 구현**: 수집된 데이터를 조회할 수 있는 REST API 엔드포인트 개발
- [ ] **Docker Compose 도입**: `Redis`, `Celery`, `App`을 한 번에 실행할 수 있는 환경 구성
- [ ] **Celery 작업 모니터링**: Flower 등을 이용한 Celery 작업 추적 및 관리 기능 추가
- [ ] **테스트 코드 작성**: 주요 서비스 로직에 대한 단위/통합 테스트 코드 추가
