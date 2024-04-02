FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

COPY wait_for_db.sh /usr/local/bin/

COPY alembic.ini .

RUN addgroup -g 1000 -S appgroup \
  && adduser -u 1000 -S appuser -G appgroup \
  && mkdir -p ./data \
  && chown -R appuser:appgroup ./data \
  && chmod -R 777 ./data/ \
  && chown appuser:appgroup alembic.ini \
  && chmod 777 alembic.ini \
  && chmod +x /usr/local/bin/wait_for_db.sh

COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV ENV "dev"

ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

CMD ["sh","-c", "/usr/local/bin/wait_for_db.sh db 5432 python main.py --reload"]

