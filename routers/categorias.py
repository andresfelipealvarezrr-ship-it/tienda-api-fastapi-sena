from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str


categorias = [
    {"id": 1, "nombre": "Perifericos"},
    {"id": 2, "nombre": "Pantallas"},
    {"id": 3, "nombre": "Audio"},
]

siguiente_id = 4


def buscar_indice_categoria(categoria_id: int):
    """Devuelve el índice de la categoría o None si no se encuentra."""
    for indice, categoria in enumerate(categorias):
        if categoria["id"] == categoria_id:
            return indice
    return None


@router.get("")
def listar_categorias():
    return categorias


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    indice = buscar_indice_categoria(categoria_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categorias[indice]


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaEntrada):
    global siguiente_id

    nueva_categoria = {"id": siguiente_id, **categoria.model_dump()}
    categorias.append(nueva_categoria)
    siguiente_id += 1
    return nueva_categoria


@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, categoria: CategoriaEntrada):
    indice = buscar_indice_categoria(categoria_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    categoria_actualizada = {"id": categoria_id, **categoria.model_dump()}
    categorias[indice] = categoria_actualizada
    return categoria_actualizada


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    indice = buscar_indice_categoria(categoria_id)
    if indice is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categorias.pop(indice)
