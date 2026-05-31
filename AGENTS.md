# AGENTS.md

## What this repo is

- Spanish-language reference documentation for **MERP** (*Middle-earth Role Playing*, a tabletop RPG).
- No code, build system, tests, or package manager. Every file is Markdown prose and table transcriptions.

## Working conventions

- **Language:** All content is in Spanish. Use Spanish when editing or adding files.
- **Naming:** Files use descriptive Spanish titles with spaces replaced by underscores (e.g. `Tablas_de_Críticos_MERP_en_Formato_JSON.md`).
- **References:** Docs cite manual tables with codes like **AT-1**, **CT-2**, **FT-3**, **BT-5**, etc. Preserve these references when editing.
- **Data directory:** `datos/` contains real JSON files with canonical game data (tables BT-1, BT-2, BT-3, BT-5, CGT-3, ST-1, ET-5, CST-1, armors, professions). These are the machine-readable data layer. Update them if source manuals correct values.

## Docker

- **Comando:** usar `docker compose` (v2, con espacio), NO `docker-compose` (v1 obsoleto).
- **Construir y levantar:** `docker compose up --build -d`
- **Ver logs:** `docker compose logs app`
- **Detener:** `docker compose down`
- La app unificada corre en `http://localhost:8000` — backend API + frontend SPA en un solo contenedor.
- Base de datos SQLite persistente via volumen: `./backend/merp.db:/app/merp.db`

## Desarrollo local (sin Docker)

```bash
cd frontend && pnpm install && pnpm build   # compilar SPA
cd ../backend && uvicorn main:app --reload   # http://localhost:8000
```

Herramientas necesarias: `uv` (Python), `pnpm` (Node.js).

## What not to do

- Do not run `npm`, `pip`, `make`, `cargo`, or any build/test/lint commands. Nothing will exist to run.
