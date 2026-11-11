import unittest

from fastapi import HTTPException
from pydantic import ValidationError

from main import app, inicio
from routers import categorias, productos


class PruebasApiTienda(unittest.TestCase):
    def test_ruta_principal_y_crud_productos(self):
        self.assertIn("funciona", inicio()["mensaje"])
        self.assertGreaterEqual(len(productos.listar_productos()), 3)

        nuevo_producto = productos.crear_producto(
            productos.ProductoEntrada(
                nombre="Webcam HD", precio=150000, categoria="Perifericos"
            )
        )
        producto_id = nuevo_producto["id"]

        self.assertEqual(productos.obtener_producto(producto_id)["nombre"], "Webcam HD")

        actualizado = productos.actualizar_producto(
            producto_id,
            productos.ProductoEntrada(
                nombre="Webcam Full HD", precio=160000, categoria="Perifericos"
            ),
        )
        self.assertEqual(actualizado["precio"], 160000)
        self.assertEqual(productos.eliminar_producto(producto_id)["id"], producto_id)

    def test_validacion_y_error_de_producto(self):
        with self.assertRaises(ValidationError):
            productos.ProductoEntrada(nombre="Producto sin precio", categoria="Audio")

        with self.assertRaises(HTTPException) as error:
            productos.obtener_producto(999)
        self.assertEqual(error.exception.status_code, 404)

    def test_crud_categorias(self):
        self.assertGreaterEqual(len(categorias.listar_categorias()), 3)

        nueva_categoria = categorias.crear_categoria(
            categorias.CategoriaEntrada(nombre="Camaras")
        )
        categoria_id = nueva_categoria["id"]

        self.assertEqual(categorias.obtener_categoria(categoria_id)["nombre"], "Camaras")

        actualizada = categorias.actualizar_categoria(
            categoria_id, categorias.CategoriaEntrada(nombre="Camaras y video")
        )
        self.assertEqual(actualizada["nombre"], "Camaras y video")
        self.assertEqual(categorias.eliminar_categoria(categoria_id)["id"], categoria_id)

    def test_validacion_y_error_de_categoria(self):
        with self.assertRaises(ValidationError):
            categorias.CategoriaEntrada()

        with self.assertRaises(HTTPException) as error:
            categorias.obtener_categoria(999)
        self.assertEqual(error.exception.status_code, 404)

    def test_rutas_y_codigos_de_creacion(self):
        rutas_productos = {ruta.path: ruta for ruta in productos.router.routes}
        rutas_categorias = {ruta.path: ruta for ruta in categorias.router.routes}
        documentacion = app.openapi()

        self.assertEqual(rutas_productos["/productos"].status_code, 201)
        self.assertEqual(rutas_categorias["/categorias"].status_code, 201)
        self.assertEqual(
            set(documentacion["paths"]),
            {
                "/",
                "/productos",
                "/productos/{producto_id}",
                "/categorias",
                "/categorias/{categoria_id}",
            },
        )
        self.assertEqual(
            set(documentacion["paths"]["/productos"]), {"get", "post"}
        )
        self.assertEqual(
            set(documentacion["paths"]["/productos/{producto_id}"]),
            {"get", "put", "delete"},
        )
        self.assertEqual(
            set(documentacion["paths"]["/categorias"]), {"get", "post"}
        )
        self.assertEqual(
            set(documentacion["paths"]["/categorias/{categoria_id}"]),
            {"get", "put", "delete"},
        )
        self.assertIn(
            "422",
            documentacion["paths"]["/productos"]["post"]["responses"],
        )
        self.assertIn(
            "422",
            documentacion["paths"]["/categorias"]["post"]["responses"],
        )


if __name__ == "__main__":
    unittest.main()
