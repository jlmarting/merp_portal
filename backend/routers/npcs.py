from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
from database import get_db
from models import Usuario, NPC
from auth import get_current_user, require_dj

router = APIRouter(prefix="/npcs", tags=["npcs"])


class CrearNPCRequest(BaseModel):
    partida_id: int
    nombre: str
    raza: str | None = None
    profesion: str | None = None
    nivel: int = 1
    datos_json: dict[str, Any] = {}
    pv: int = 0
    pp: int = 0
    tipo: str = "enemigo"


@router.post("")
@router.post("/")
def crear_npc(
    req: CrearNPCRequest,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    npc = NPC(
        partida_id=req.partida_id,
        creado_por_id=current_user.id,
        nombre=req.nombre,
        raza=req.raza,
        profesion=req.profesion,
        nivel=req.nivel,
        datos_json=req.datos_json,
        pv=req.pv,
        pp=req.pp,
        tipo=req.tipo,
    )
    db.add(npc)
    db.commit()
    db.refresh(npc)
    return {"id": npc.id, "nombre": npc.nombre}


@router.get("/")
def listar_npcs(
    partida_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    npcs = db.query(NPC).filter(NPC.partida_id == partida_id).all()
    return [
        {
            "id": n.id,
            "nombre": n.nombre,
            "raza": n.raza,
            "profesion": n.profesion,
            "nivel": n.nivel,
            "pv": n.pv,
            "pp": n.pp,
            "tipo": n.tipo,
            "es_participante_combate": n.es_participante_combate,
        }
        for n in npcs
    ]


@router.get("/{npc_id}")
def obtener_npc(npc_id: int, db: Session = Depends(get_db)):
    n = db.query(NPC).filter(NPC.id == npc_id).first()
    if not n:
        raise HTTPException(status_code=404)
    return {
        "id": n.id,
        "nombre": n.nombre,
        "raza": n.raza,
        "profesion": n.profesion,
        "nivel": n.nivel,
        "datos_json": n.datos_json,
        "pv": n.pv,
        "pp": n.pp,
        "tipo": n.tipo,
        "es_participante_combate": n.es_participante_combate,
    }


@router.put("/{npc_id}")
def actualizar_npc(
    npc_id: int,
    req: CrearNPCRequest,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    n = db.query(NPC).filter(NPC.id == npc_id).first()
    if not n:
        raise HTTPException(status_code=404)

    n.nombre = req.nombre
    n.raza = req.raza
    n.profesion = req.profesion
    n.nivel = req.nivel
    n.datos_json = req.datos_json
    n.pv = req.pv
    n.pp = req.pp
    n.tipo = req.tipo
    db.commit()
    return {"mensaje": "NPC actualizado"}


@router.delete("/{npc_id}")
def eliminar_npc(
    npc_id: int,
    current_user: Usuario = Depends(require_dj),
    db: Session = Depends(get_db),
):
    n = db.query(NPC).filter(NPC.id == npc_id).first()
    if not n:
        raise HTTPException(status_code=404)
    db.delete(n)
    db.commit()
    return {"mensaje": "NPC eliminado"}
