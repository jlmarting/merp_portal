from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from database import get_db
from models import Usuario, Partida, SesionCombate
from auth import get_current_user, require_dj

router = APIRouter(prefix="/sesiones", tags=["sesiones"])


class CrearSesionRequest(BaseModel):
    partida_id: int
    nombre: str


@router.post("")
@router.post("/")
def crear_sesion(
    req: CrearSesionRequest,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    sesion = SesionCombate(
        partida_id=req.partida_id,
        nombre=req.nombre,
    )
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return {
        "id": sesion.id,
        "nombre": sesion.nombre,
        "estado": sesion.estado,
    }


@router.get("/")
def listar_sesiones(partida_id: int, db: Session = Depends(get_db)):
    sesiones = (
        db.query(SesionCombate)
        .filter(SesionCombate.partida_id == partida_id)
        .order_by(SesionCombate.fecha_inicio.desc())
        .all()
    )
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "fecha_inicio": s.fecha_inicio.isoformat(),
            "fecha_fin": s.fecha_fin.isoformat() if s.fecha_fin else None,
            "estado": s.estado,
        }
        for s in sesiones
    ]


@router.get("/{sesion_id}")
def obtener_sesion(sesion_id: int, db: Session = Depends(get_db)):
    s = db.query(SesionCombate).filter(SesionCombate.id == sesion_id).first()
    if not s:
        raise HTTPException(status_code=404)
    return {
        "id": s.id,
        "nombre": s.nombre,
        "fecha_inicio": s.fecha_inicio.isoformat(),
        "fecha_fin": s.fecha_fin.isoformat() if s.fecha_fin else None,
        "estado": s.estado,
    }


class CerrarSesionRequest(BaseModel):
    estado: str = "cerrada"


@router.put("/{sesion_id}")
def cerrar_sesion(
    sesion_id: int,
    req: CerrarSesionRequest,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    s = db.query(SesionCombate).filter(SesionCombate.id == sesion_id).first()
    if not s:
        raise HTTPException(status_code=404)
    s.estado = req.estado
    if req.estado == "cerrada":
        s.fecha_fin = datetime.utcnow()
    db.commit()
    return {"mensaje": "Sesión actualizada"}
