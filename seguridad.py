from datetime import datetime, timedelta, timezone
from os import getenv
from secrets import token_urlsafe
from threading import Lock
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = getenv("JWT_SECRET_KEY") or token_urlsafe(48)
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30


def hashear_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verificar_password(password: str, hash_guardado: str) -> bool:
    password_bytes = password.encode("utf-8")
    return len(password_bytes) <= 72 and bcrypt.checkpw(
        password_bytes, hash_guardado.encode("ascii")
    )


# Cuentas disponibles únicamente para las pruebas del proyecto académico.
usuarios = {
    "admin": {"username": "admin", "nombre": "Administrador",
              "password_hash": hashear_password("admin123"), "rol": "admin"},
    "ana": {"username": "ana", "nombre": "Ana Cliente",
            "password_hash": hashear_password("ana123"), "rol": "cliente"},
}
registro_lock = Lock()


def buscar_usuario(username: str):
    return usuarios.get(username)


def registrar_usuario(username: str, nombre: str, password: str):
    password_hash = hashear_password(password)
    with registro_lock:
        if username in usuarios:
            raise HTTPException(status_code=409, detail="El usuario ya existe")

        usuario = {"username": username, "nombre": nombre,
                   "password_hash": password_hash, "rol": "cliente"}
        usuarios[username] = usuario
    return usuario


def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode({"sub": username, "exp": expira}, SECRET_KEY, algorithm=ALGORITMO)


oauth2_esquema = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def error_401(detalle: str) -> HTTPException:
    return HTTPException(
        status_code=401, detail=detalle, headers={"WWW-Authenticate": "Bearer"}
    )


def obtener_usuario_actual(token: Annotated[str | None, Depends(oauth2_esquema)]):
    if not token:
        raise error_401("Se requiere un token de acceso")
    try:
        datos = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITMO], options={"require": ["sub", "exp"]}
        )
    except jwt.InvalidTokenError:
        raise error_401("Token inválido o vencido") from None

    usuario = buscar_usuario(datos["sub"])
    if usuario is None:
        raise error_401("Usuario del token no encontrado")
    return usuario


UsuarioActual = Annotated[dict, Depends(obtener_usuario_actual)]


def requerir_admin(usuario: UsuarioActual):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol de administrador")
    return usuario
