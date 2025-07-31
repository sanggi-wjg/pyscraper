# PyScraper

## Installation

```shell
poetry install

celery -A app.config.celery worker --loglevel=INFO
celery -A app.config.celery beat   --loglevel=INFO
```

## TODO

- [ ] Add a docker-compose ?
- [ ] Celery results ?
- [ ] Add tests ?
