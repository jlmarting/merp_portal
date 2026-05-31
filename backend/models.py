import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="jugador")  # jugador, dj, lector
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    partida = relationship(
        "Partida", back_populates="usuarios", foreign_keys=[partida_id]
    )
    personajes = relationship("Personaje", back_populates="usuario")


class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    dj_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    usuarios = relationship(
        "Usuario", back_populates="partida", foreign_keys="Usuario.partida_id"
    )
    personajes = relationship("Personaje", back_populates="partida")
    npcs = relationship("NPC", back_populates="partida")
    sesiones_combate = relationship("SesionCombate", back_populates="partida")
    dj = relationship("Usuario", foreign_keys=[dj_id])


class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    raza = Column(String(50), nullable=False)
    profesion = Column(String(50), nullable=False)
    nivel = Column(Integer, default=1)
    experiencia = Column(Integer, default=0)
    datos_json = Column(JSON, nullable=False)
    pv_actuales = Column(Integer, default=0)
    pv_maximos = Column(Integer, default=0)
    pp_actuales = Column(Integer, default=0)
    pp_maximos = Column(Integer, default=0)
    estado = Column(
        String(20), default="vivo"
    )  # vivo, muerto, incapacitado, inconsciente
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    usuario = relationship("Usuario", back_populates="personajes")
    partida = relationship("Partida", back_populates="personajes")
    acciones = relationship("AccionCombate", back_populates="personaje")
    sortilegios = relationship("SortilegioPersonaje", back_populates="personaje")


class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    creado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    raza = Column(String(50), nullable=True)
    profesion = Column(String(50), nullable=True)
    nivel = Column(Integer, default=1)
    datos_json = Column(JSON, nullable=False)
    pv = Column(Integer, default=0)
    pp = Column(Integer, default=0)
    tipo = Column(String(20), default="enemigo")  # enemigo, aliado, neutral
    es_participante_combate = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    partida = relationship("Partida", back_populates="npcs")
    creado_por = relationship("Usuario")
    acciones = relationship("AccionCombate", back_populates="npc")


class SesionCombate(Base):
    __tablename__ = "sesiones_combate"

    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(String(20), default="activa")  # activa, cerrada

    partida = relationship("Partida", back_populates="sesiones_combate")
    acciones = relationship("AccionCombate", back_populates="sesion")


class AccionCombate(Base):
    __tablename__ = "acciones_combate"

    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones_combate.id"), nullable=False)
    personaje_id = Column(Integer, ForeignKey("personajes.id"), nullable=True)
    npc_id = Column(Integer, ForeignKey("npcs.id"), nullable=True)
    tipo_accion = Column(
        String(30), nullable=False
    )  # ataque_fisico, ataque_magico, maniobra, sortilegio, otro
    tirada_sin_modificar = Column(Integer, nullable=True)
    modificadores_json = Column(JSON, nullable=True)
    resultado_final = Column(Integer, nullable=True)
    tabla_ataque = Column(String(10), nullable=True)
    tipo_armadura_oponente = Column(Integer, nullable=True)
    resultado_tabla = Column(String(10), nullable=True)
    dano = Column(Integer, default=0)
    critico = Column(Boolean, default=False)
    tipo_critico = Column(String(30), nullable=True)
    gravedad_critico = Column(String(5), nullable=True)
    tirada_critico = Column(Integer, nullable=True)
    efecto_critico = Column(Text, nullable=True)
    descripcion = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    sesion = relationship("SesionCombate", back_populates="acciones")
    personaje = relationship("Personaje", back_populates="acciones")
    npc = relationship("NPC", back_populates="acciones")


class SortilegioPersonaje(Base):
    __tablename__ = "sortilegios_personaje"

    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"), nullable=False)
    sortilegio_nombre = Column(String(100), nullable=False)
    lista_nombre = Column(String(100), nullable=True)
    circulo = Column(Integer, default=1)
    grado_conocido = Column(Integer, default=1)

    personaje = relationship("Personaje", back_populates="sortilegios")
