from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from models import Usuario
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    rol: str


@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.username == req.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == req.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    user = Usuario(
        username=req.username,
        email=req.email,
        password_hash=hash_password(req.password),
        rol="jugador",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return AuthResponse(
        access_token=token, user_id=user.id, username=user.username, rol=user.rol
    )


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = create_access_token({"sub": str(user.id)})
    return AuthResponse(
        access_token=token, user_id=user.id, username=user.username, rol=user.rol
    )


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    rol: str
    partida_id: int | None = None


@router.get("/me", response_model=UserInfo)
def me(current_user: Usuario = Depends(get_current_user)):
    return UserInfo(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        rol=current_user.rol,
        partida_id=current_user.partida_id,
    )
