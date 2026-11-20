from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

import seguridad


router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


class ProveedorEntrada(BaseModel):
    nombre: str


proveedores = [
    {"id": 1, "nombre": "Distribuciones Andinas"},
    {"id": 2, "nombre": "Tecno Mayorista"},
    {"id": 3, "nombre": "Suministros Digitales"},
]

siguiente_id = 4


def buscar_indice_proveedor(proveedor_id: int):
    """Devuelve el índice del proveedor o None si no se encuentra."""
    for indice, proveedor in enumerate(proveedores):
        if proveedor["id"] == proveedor_id:
            return indice
    return None


@router.get("")
def listar_proveedores():
    return proveedores


@router.get("/{proveedor_id}")
def obtener_proveedor(proveedor_id: int):
    indice = buscar_indice_proveedor(proveedor_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedores[indice]


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(seguridad.obtener_usuario_actual)])
def crear_proveedor(proveedor: ProveedorEntrada):
    global siguiente_id

    nuevo_proveedor = {"id": siguiente_id, **proveedor.model_dump()}
    proveedores.append(nuevo_proveedor)
    siguiente_id += 1
    return nuevo_proveedor


@router.put("/{proveedor_id}", dependencies=[Depends(seguridad.obtener_usuario_actual)])
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorEntrada):
    indice = buscar_indice_proveedor(proveedor_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    proveedor_actualizado = {"id": proveedor_id, **proveedor.model_dump()}
    proveedores[indice] = proveedor_actualizado
    return proveedor_actualizado


@router.delete("/{proveedor_id}", dependencies=[Depends(seguridad.requerir_admin)])
def eliminar_proveedor(proveedor_id: int):
    indice = buscar_indice_proveedor(proveedor_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return proveedores.pop(indice)
