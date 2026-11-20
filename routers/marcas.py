from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

import seguridad


router = APIRouter(prefix="/marcas", tags=["Marcas"])


class MarcaEntrada(BaseModel):
    nombre: str


marcas = [
    {"id": 1, "nombre": "Logitech"},
    {"id": 2, "nombre": "Samsung"},
    {"id": 3, "nombre": "HyperX"},
]

siguiente_id = 4


def buscar_indice_marca(marca_id: int):
    """Devuelve el índice de la marca o None si no se encuentra."""
    for indice, marca in enumerate(marcas):
        if marca["id"] == marca_id:
            return indice
    return None


@router.get("")
def listar_marcas():
    return marcas


@router.get("/{marca_id}")
def obtener_marca(marca_id: int):
    indice = buscar_indice_marca(marca_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marcas[indice]


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(seguridad.obtener_usuario_actual)])
def crear_marca(marca: MarcaEntrada):
    global siguiente_id

    nueva_marca = {"id": siguiente_id, **marca.model_dump()}
    marcas.append(nueva_marca)
    siguiente_id += 1
    return nueva_marca


@router.put("/{marca_id}", dependencies=[Depends(seguridad.obtener_usuario_actual)])
def actualizar_marca(marca_id: int, marca: MarcaEntrada):
    indice = buscar_indice_marca(marca_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    marca_actualizada = {"id": marca_id, **marca.model_dump()}
    marcas[indice] = marca_actualizada
    return marca_actualizada


@router.delete("/{marca_id}", dependencies=[Depends(seguridad.requerir_admin)])
def eliminar_marca(marca_id: int):
    indice = buscar_indice_marca(marca_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    return marcas.pop(indice)
