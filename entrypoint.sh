#!/bin/sh

echo "🚀 Iniciando o processo de migração do banco de dados..."
poetry run alembic upgrade head
echo "✅ Migração concluída com sucesso."

echo "🔥 Iniciando o servidor FastAPI com Uvicorn..."
poetry run uvicorn --host 0.0.0.0 --port 8000 app.app:app