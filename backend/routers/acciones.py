from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any, Optional
from database import get_db
from models import Usuario, AccionCombate, SesionCombate
from auth import get_current_user

router = APIRouter(prefix="/sesiones/{sesion_id}/acciones", tags=["acciones"])


class RegistrarAccionRequest(BaseModel):
    personaje_id: int | None = None
    npc_id: int | None = None
    tipo_accion: str
    tirada_sin_modificar: int | None = None
    modificadores_json: dict[str, Any] = {}
    resultado_final: int | None = None
    tabla_ataque: str | None = None
    tipo_armadura_oponente: int | None = None
    resultado_tabla: str | None = None
    dano: int = 0
    critico: bool = False
    tipo_critico: str | None = None
    gravedad_critico: str | None = None
    tirada_critico: int | None = None
    efecto_critico: str | None = None
    descripcion: str | None = None


@router.post("")
@router.post("/")
def registrar_accion(
    sesion_id: int,
    req: RegistrarAccionRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sesion = db.query(SesionCombate).filter(SesionCombate.id == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if sesion.estado == "cerrada":
        raise HTTPException(status_code=400, detail="La sesión está cerrada")

    accion = AccionCombate(
        sesion_id=sesion_id,
        personaje_id=req.personaje_id,
        npc_id=req.npc_id,
        tipo_accion=req.tipo_accion,
        tirada_sin_modificar=req.tirada_sin_modificar,
        modificadores_json=req.modificadores_json,
        resultado_final=req.resultado_final,
        tabla_ataque=req.tabla_ataque,
        tipo_armadura_oponente=req.tipo_armadura_oponente,
        resultado_tabla=req.resultado_tabla,
        dano=req.dano,
        critico=req.critico,
        tipo_critico=req.tipo_critico,
        gravedad_critico=req.gravedad_critico,
        tirada_critico=req.tirada_critico,
        efecto_critico=req.efecto_critico,
        descripcion=req.descripcion,
    )
    db.add(accion)
    db.commit()
    db.refresh(accion)
    return {"id": accion.id, "descripcion": accion.descripcion}


@router.get("/")
def listar_acciones(sesion_id: int, db: Session = Depends(get_db)):
    sesion = db.query(SesionCombate).filter(SesionCombate.id == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=404)

    acciones = (
        db.query(AccionCombate)
        .filter(AccionCombate.sesion_id == sesion_id)
        .order_by(AccionCombate.timestamp.asc())
        .all()
    )

    return [
        {
            "id": a.id,
            "personaje_id": a.personaje_id,
            "npc_id": a.npc_id,
            "tipo_accion": a.tipo_accion,
            "tirada_sin_modificar": a.tirada_sin_modificar,
            "modificadores_json": a.modificadores_json,
            "resultado_final": a.resultado_final,
            "tabla_ataque": a.tabla_ataque,
            "tipo_armadura_oponente": a.tipo_armadura_oponente,
            "resultado_tabla": a.resultado_tabla,
            "dano": a.dano,
            "critico": a.critico,
            "tipo_critico": a.tipo_critico,
            "gravedad_critico": a.gravedad_critico,
            "tirada_critico": a.tirada_critico,
            "efecto_critico": a.efecto_critico,
            "descripcion": a.descripcion,
            "timestamp": a.timestamp.isoformat(),
        }
        for a in acciones
    ]
