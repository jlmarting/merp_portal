from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Usuario, Partida
from auth import get_current_user, require_dj

router = APIRouter(prefix="/partidas", tags=["partidas"])


class CrearPartidaRequest(BaseModel):
    nombre: str


@router.post("")
@router.post("/")
def crear_partida(
    req: CrearPartidaRequest,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    partida = Partida(nombre=req.nombre, dj_id=current_user.id)
    db.add(partida)
    db.commit()
    db.refresh(partida)
    return {"id": partida.id, "nombre": partida.nombre}


@router.get("/")
def listar_partidas(db: Session = Depends(get_db)):
    return [
        {"id": p.id, "nombre": p.nombre, "dj_id": p.dj_id}
        for p in db.query(Partida).all()
    ]


@router.get("/{partida_id}")
def obtener_partida(partida_id: int, db: Session = Depends(get_db)):
    p = db.query(Partida).filter(Partida.id == partida_id).first()
    if not p:
        raise HTTPException(status_code=404)
    return {
        "id": p.id,
        "nombre": p.nombre,
        "dj_id": p.dj_id,
    }
