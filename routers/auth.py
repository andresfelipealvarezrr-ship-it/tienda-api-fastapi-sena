from typing import Annotated, Literal

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, StringConstraints, field_validator

import seguridad


router = APIRouter(prefix="/auth", tags=["Autenticación"])


class RegistroEntrada(BaseModel):
    username: Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z0-9_.-]{3,40}$")
    ]
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
    password: str = Field(min_length=6, max_length=72, repr=False)

    @field_validator("password")
    @classmethod
    def validar_bytes_bcrypt(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("La contraseña debe ocupar máximo 72 bytes")
        return password


class UsuarioPublico(BaseModel):
    username: str
    nombre: str
    rol: Literal["admin", "cliente"]


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


@router.post("/login", response_model=Token)
def login(datos: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(datos.password, usuario["password_hash"]):
        raise seguridad.error_401("Usuario o contraseña incorrectos")
    return Token(access_token=seguridad.crear_token(usuario["username"]))


@router.post("/registro", status_code=status.HTTP_201_CREATED, response_model=UsuarioPublico)
def registro(datos: RegistroEntrada):
    return seguridad.registrar_usuario(datos.username, datos.nombre, datos.password)


@router.get("/yo", response_model=UsuarioPublico)
def quien_soy(usuario: seguridad.UsuarioActual):
    return usuario
