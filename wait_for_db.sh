#!/bin/sh

HOST="$1"
PORT="$2"
shift 2
REST="$@"

if [ -z "$HOST" ] || [ -z "$PORT" ]; then
  echo "Usage: $0 <HOST> <PORT>"
  exit 1
fi

while ! nc -z "$HOST" "$PORT"; do
  echo "Waiting for database... <$HOST> <$PORT> <$REST>"
  sleep 1
done

  echo "tudo certo"

exec "$@"