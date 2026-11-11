from fastapi import FastAPI

from routers import categorias, productos


app = FastAPI(title="API de la Tienda")

app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/")
def inicio():
    return {"mensaje": "La API de la Tienda funciona correctamente"}
