# ==========================================
# Etapa 1: Compilación del Frontend
# ==========================================
FROM node:22-alpine AS frontend
WORKDIR /build

# Habilitamos pnpm de forma segura
RUN corepack enable && corepack prepare pnpm@10 --activate

# Copiamos solo lo necesario para instalar dependencias (Aprovechamiento de caché)
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copiamos el resto del código y compilamos
COPY frontend/ .
RUN pnpm build

# ==========================================
# Etapa 2: Imagen Final de Producción
# ==========================================
FROM python:3.12-slim

# Copiamos la herramienta UV desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY backend/requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY backend/ .
COPY --from=frontend /build/dist ./frontend/dist/

# Parámetros de entorno dinámicos y configurables
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

EXPOSE ${APP_PORT}

# Sintaxis de shell combinada con 'exec' para mantener el PID 1 (captura de SIGTERM)
CMD exec uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}
