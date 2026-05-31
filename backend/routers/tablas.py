import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/tablas", tags=["tablas"])

DATOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")

CATALOGO_TABLAS = {
    "bt1": "Tabla_BT-1.json",
    "bt2": "Tabla_BT-2.json",
    "bt3": "Tabla_BT-3.json",
    "bt5": "Tabla_BT-5.json",
    "cgt3": "Tabla_CGT-3.json",
    "st1": "Tabla_ST-1.json",
    "et5": "Tabla_ET-5.json",
    "cst1": "Tabla_CST-1.json",
    "movimiento": "Tabla_Movimiento.json",
    "profesiones": "Catalogo_Profesiones.json",
    "armaduras": "Catalogo_Armaduras.json",
    "sortilegios": "Catalogo_Sortilegios.json",
}


def _load_table(filename: str):
    path = os.path.join(DATOS_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Tabla {filename} no encontrada")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/")
def listar_tablas():
    return {
        codigo: {"archivo": archivo, "url": f"/tablas/{codigo}"}
        for codigo, archivo in CATALOGO_TABLAS.items()
    }


@router.get("/profesiones")
def profesiones():
    return _load_table(CATALOGO_TABLAS["profesiones"])


@router.get("/armas")
def armas():
    return _load_table(CATALOGO_TABLAS["cst1"])


@router.get("/armaduras")
def armaduras():
    return _load_table(CATALOGO_TABLAS["armaduras"])


@router.get("/sortilegios")
def sortilegios():
    return _load_table(CATALOGO_TABLAS["sortilegios"])


@router.get("/razas")
def razas():
    cgt3 = _load_table(CATALOGO_TABLAS["cgt3"])
    bt3 = _load_table(CATALOGO_TABLAS["bt3"])
    return {"cgt3": cgt3, "bt3": bt3}


@router.get("/{codigo}")
def obtener_tabla(codigo: str):
    if codigo not in CATALOGO_TABLAS:
        raise HTTPException(
            status_code=404,
            detail=f"Tabla '{codigo}' no existe. Usa GET /tablas/ para listado.",
        )
    return _load_table(CATALOGO_TABLAS[codigo])
