import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import (
    auth_router,
    personajes,
    npcs,
    sesiones,
    acciones,
    tablas,
    partidas,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MERP Character Portal",
    description="API para la creación y gestión de personajes de MERP",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(personajes.router)
app.include_router(npcs.router)
app.include_router(sesiones.router)
app.include_router(acciones.router)
app.include_router(tablas.router)
app.include_router(partidas.router)

STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "frontend", "dist"
)
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist"
    )

if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

    API_PATHS = (
        "/auth",
        "/personajes",
        "/npcs",
        "/sesiones",
        "/tablas",
        "/partidas",
        "/docs",
        "/openapi",
        "/redoc",
    )

    @app.middleware("http")
    async def spa_fallback(request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404 and not request.url.path.startswith(API_PATHS):
            index = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(index):
                return FileResponse(index, media_type="text/html")
        return response
