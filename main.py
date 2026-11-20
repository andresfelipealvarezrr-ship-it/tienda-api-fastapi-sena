from fastapi import FastAPI

from routers import auth, categorias, marcas, productos, proveedores


app = FastAPI(title="API de la Tienda")

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(marcas.router)
app.include_router(proveedores.router)


@app.get("/")
def inicio():
    return {"mensaje": "La API de la Tienda funciona correctamente"}
