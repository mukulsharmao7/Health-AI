FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir . \
    && useradd --create-home --uid 10001 app \
    && chown -R app:app /app

USER 10001:10001
EXPOSE 10000
CMD ["sh", "scripts/start.sh"]
