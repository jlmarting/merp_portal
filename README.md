# MERP Character Portal

Portal web para crear y gestionar personajes de *Middle-earth Role Playing* (MERP).

---

## Requisitos

- Docker (con `docker compose` v2)

## Inicio rápido

```bash
docker compose up --build -d
```

Abrir http://localhost:8000

### Registrar primer usuario

1. Ir a http://localhost:8000/register
2. Crear cuenta (usuario, email, contraseña)
3. Iniciar sesión en http://localhost:8000/login

---

## Desarrollo local (sin Docker)

```bash
# Terminal 1 — Backend
cd backend
uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
pnpm install
pnpm dev
```

Abrir http://localhost:5173

---

## Estructura

```
backend/     — API FastAPI + SQLite
frontend/    — SPA Vue 3 + Vite + TypeScript
datos/       — datos canónicos del juego (JSON)
origin/      — documentación de referencia
```
