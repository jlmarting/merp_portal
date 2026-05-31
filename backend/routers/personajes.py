from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
from database import get_db
from models import Usuario, Personaje, SortilegioPersonaje
from auth import get_current_user, require_dj

router = APIRouter(prefix="/personajes", tags=["personajes"])


class DesgloseHabilidad(BaseModel):
    grado: int
    carac: int
    profesion: int
    objeto: int
    especial: int
    total: int


class Caracteristica(BaseModel):
    valor_base: int
    bonif_normal: int
    bonif_raza: int
    total: int
    bono: int


class Arma(BaseModel):
    nombre: str
    tipo: str
    tabla_ataque: str
    tipo_critico: str
    rango_pifia: list[int]
    bonificacion: int
    factor_parada: int
    manos: int
    peso_kg: float


class Armadura(BaseModel):
    nombre: str
    tipo_armadura: int
    penalizacion_mm: int
    peso_kg: float
    categoria: str


class Escudo(BaseModel):
    nombre: str
    penalizacion_mm: int
    peso_kg: float
    bonificacion_defensiva: int


class EquipoData(BaseModel):
    armas: list[Arma]
    armadura: Armadura | None = None
    escudo: Escudo | None = None
    peso_total: float = 0


class CrearPersonajeRequest(BaseModel):
    partida_id: int
    nombre: str
    raza: str
    profesion: str
    nivel: int = 1
    experiencia: int = 0
    caracteristicas: dict[str, Caracteristica]
    habilidades: dict[str, DesgloseHabilidad]
    equipo: EquipoData
    desarrollo_fisico: int
    desarrollo_poder: int
    pv_actuales: int
    pv_maximos: int
    pp_actuales: int
    pp_maximos: int
    estado: str = "vivo"
    movimiento_base: int = 10
    sortilegios: list[dict[str, Any]] = []


@router.post("")
@router.post("/")
def crear_personaje(
    req: CrearPersonajeRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    personaje = Personaje(
        usuario_id=current_user.id,
        partida_id=req.partida_id,
        nombre=req.nombre,
        raza=req.raza,
        profesion=req.profesion,
        nivel=req.nivel,
        experiencia=req.experiencia,
        datos_json={
            "caracteristicas": {
                k: v.model_dump() for k, v in req.caracteristicas.items()
            },
            "habilidades": {k: v.model_dump() for k, v in req.habilidades.items()},
            "equipo": req.equipo.model_dump(),
            "desarrollo_fisico": req.desarrollo_fisico,
            "desarrollo_poder": req.desarrollo_poder,
            "movimiento_base": req.movimiento_base,
        },
        pv_actuales=req.pv_actuales,
        pv_maximos=req.pv_maximos,
        pp_actuales=req.pp_actuales,
        pp_maximos=req.pp_maximos,
        estado=req.estado,
    )
    db.add(personaje)
    db.flush()

    for s in req.sortilegios:
        db.add(
            SortilegioPersonaje(
                personaje_id=personaje.id,
                sortilegio_nombre=s["sortilegio_nombre"],
                lista_nombre=s.get("lista_nombre"),
                circulo=s.get("circulo", 1),
                grado_conocido=s.get("grado_conocido", 1),
            )
        )

    db.commit()
    db.refresh(personaje)
    return {"id": personaje.id, "nombre": personaje.nombre}


@router.get("/mis")
def mis_personajes(
    current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)
):
    personajes = (
        db.query(Personaje).filter(Personaje.usuario_id == current_user.id).all()
    )
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "raza": p.raza,
            "profesion": p.profesion,
            "nivel": p.nivel,
            "estado": p.estado,
            "pv_actuales": p.pv_actuales,
            "pv_maximos": p.pv_maximos,
        }
        for p in personajes
    ]


@router.get("/{personaje_id}")
def obtener_personaje(
    personaje_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    p = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    if p.usuario_id != current_user.id and current_user.rol != "dj":
        raise HTTPException(status_code=403, detail="No tienes acceso a este personaje")

    sortilegios = (
        db.query(SortilegioPersonaje)
        .filter(SortilegioPersonaje.personaje_id == p.id)
        .all()
    )

    return {
        "id": p.id,
        "nombre": p.nombre,
        "raza": p.raza,
        "profesion": p.profesion,
        "nivel": p.nivel,
        "experiencia": p.experiencia,
        "estado": p.estado,
        "pv_actuales": p.pv_actuales,
        "pv_maximos": p.pv_maximos,
        "pp_actuales": p.pp_actuales,
        "pp_maximos": p.pp_maximos,
        "datos_json": p.datos_json,
        "sortilegios": [
            {
                "id": s.id,
                "sortilegio_nombre": s.sortilegio_nombre,
                "lista_nombre": s.lista_nombre,
                "circulo": s.circulo,
                "grado_conocido": s.grado_conocido,
            }
            for s in sortilegios
        ],
    }


@router.put("/{personaje_id}")
def actualizar_personaje(
    personaje_id: int,
    req: CrearPersonajeRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    p = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    if p.usuario_id != current_user.id and current_user.rol != "dj":
        raise HTTPException(status_code=403, detail="No tienes acceso a este personaje")

    p.nombre = req.nombre
    p.raza = req.raza
    p.profesion = req.profesion
    p.nivel = req.nivel
    p.experiencia = req.experiencia
    p.datos_json = {
        "caracteristicas": {k: v.model_dump() for k, v in req.caracteristicas.items()},
        "habilidades": {k: v.model_dump() for k, v in req.habilidades.items()},
        "equipo": req.equipo.model_dump(),
        "desarrollo_fisico": req.desarrollo_fisico,
        "desarrollo_poder": req.desarrollo_poder,
        "movimiento_base": req.movimiento_base,
    }
    p.pv_actuales = req.pv_actuales
    p.pv_maximos = req.pv_maximos
    p.pp_actuales = req.pp_actuales
    p.pp_maximos = req.pp_maximos
    p.estado = req.estado

    db.query(SortilegioPersonaje).filter(
        SortilegioPersonaje.personaje_id == p.id
    ).delete()
    for s in req.sortilegios:
        db.add(
            SortilegioPersonaje(
                personaje_id=p.id,
                sortilegio_nombre=s["sortilegio_nombre"],
                lista_nombre=s.get("lista_nombre"),
                circulo=s.get("circulo", 1),
                grado_conocido=s.get("grado_conocido", 1),
            )
        )

    db.commit()
    return {"mensaje": "Personaje actualizado"}


@router.delete("/{personaje_id}")
def eliminar_personaje(
    personaje_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    p = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not p:
        raise HTTPException(status_code=404)
    if p.usuario_id != current_user.id and current_user.rol != "dj":
        raise HTTPException(status_code=403)

    db.delete(p)
    db.commit()
    return {"mensaje": "Personaje eliminado"}
