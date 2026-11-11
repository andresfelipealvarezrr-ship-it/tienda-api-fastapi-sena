from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str


productos = [
    {
        "id": 1,
        "nombre": "Teclado mecanico",
        "precio": 120000,
        "categoria": "Perifericos",
    },
    {
        "id": 2,
        "nombre": "Mouse gamer",
        "precio": 85000,
        "categoria": "Perifericos",
    },
    {
        "id": 3,
        "nombre": "Monitor 24",
        "precio": 650000,
        "categoria": "Pantallas",
    },
]

siguiente_id = 4


def buscar_indice_producto(producto_id: int):
    """Devuelve el índice del producto o None si no se encuentra."""
    for indice, producto in enumerate(productos):
        if producto["id"] == producto_id:
            return indice
    return None


@router.get("")
def listar_productos():
    return productos


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    indice = buscar_indice_producto(producto_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productos[indice]


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoEntrada):
    global siguiente_id

    nuevo_producto = {"id": siguiente_id, **producto.model_dump()}
    productos.append(nuevo_producto)
    siguiente_id += 1
    return nuevo_producto


@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, producto: ProductoEntrada):
    indice = buscar_indice_producto(producto_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_actualizado = {"id": producto_id, **producto.model_dump()}
    productos[indice] = producto_actualizado
    return producto_actualizado


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int):
    indice = buscar_indice_producto(producto_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return productos.pop(indice)
