from datetime import datetime, timedelta, timezone
import unittest

from fastapi.testclient import TestClient
import jwt

from main import app
import seguridad


cliente = TestClient(app)

RECURSOS = {
    "/productos": {"nombre": "Webcam HD", "precio": 150000, "categoria": "Perifericos"},
    "/categorias": {"nombre": "Cámaras"},
    "/marcas": {"nombre": "Marca de prueba"},
    "/proveedores": {"nombre": "Proveedor de prueba"},
}


def cabecera_login(username, password):
    respuesta = cliente.post("/auth/login", data={"username": username, "password": password})
    respuesta.raise_for_status()
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


class PruebasApiTienda(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ana = cabecera_login("ana", "ana123")
        cls.admin = cabecera_login("admin", "admin123")

    def test_crud_y_permisos_de_los_cuatro_recursos(self):
        self.assertIn("funciona", cliente.get("/").json()["mensaje"])
        for ruta, datos in RECURSOS.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(cliente.get(ruta).status_code, 200)
                self.assertEqual(cliente.get(f"{ruta}/1").status_code, 200)
                self.assertEqual(cliente.get(f"{ruta}/999999").status_code, 404)
                sin_token = cliente.post(ruta, json=datos)
                self.assertEqual(sin_token.status_code, 401)
                self.assertEqual(sin_token.headers["WWW-Authenticate"], "Bearer")
                self.assertEqual(cliente.post(ruta, json={}, headers=self.ana).status_code, 422)

                creado = cliente.post(ruta, json=datos, headers=self.ana)
                self.assertEqual(creado.status_code, 201)
                if ruta == "/productos":
                    self.assertEqual(creado.json()["creado_por"], "ana")
                individual = f"{ruta}/{creado.json()['id']}"
                self.assertEqual(cliente.get(individual).json()["nombre"], datos["nombre"])
                cambio = {**datos, "nombre": "Nombre actualizado"}
                self.assertEqual(cliente.put(individual, json=cambio).status_code, 401)
                actualizado = cliente.put(individual, json=cambio, headers=self.ana)
                self.assertEqual(actualizado.status_code, 200)
                self.assertEqual(actualizado.json()["nombre"], cambio["nombre"])
                self.assertEqual(cliente.delete(individual).status_code, 401)
                self.assertEqual(cliente.delete(individual, headers=self.ana).status_code, 403)
                self.assertEqual(cliente.delete(individual, headers=self.admin).status_code, 200)
                self.assertEqual(cliente.get(individual).status_code, 404)

    def test_registro_obliga_rol_cliente_y_guarda_hash(self):
        datos = {"username": "prueba_guia", "nombre": "Usuario de prueba",
                 "password": "prueba123", "rol": "admin"}
        registrado = cliente.post("/auth/registro", json=datos)
        self.assertEqual(registrado.status_code, 201)
        self.assertEqual(registrado.json(), {
            "username": datos["username"], "nombre": datos["nombre"], "rol": "cliente"
        })
        self.assertEqual(cliente.post("/auth/registro", json=datos).status_code, 409)
        hash_guardado = seguridad.buscar_usuario(datos["username"])["password_hash"]
        self.assertNotEqual(hash_guardado, datos["password"])
        self.assertTrue(seguridad.verificar_password(datos["password"], hash_guardado))

        cabecera = cabecera_login(datos["username"], datos["password"])
        yo = cliente.get("/auth/yo", headers=cabecera)
        self.assertEqual(yo.status_code, 200)
        self.assertEqual(yo.json(), registrado.json())
        self.assertEqual(cliente.delete("/productos/1", headers=cabecera).status_code, 403)

    def test_login_incorrecto_y_tokens_invalidos(self):
        fallo = cliente.post("/auth/login", data={"username": "ana", "password": "incorrecta"})
        self.assertEqual(fallo.status_code, 401)
        vencido = jwt.encode(
            {"sub": "ana", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
            seguridad.SECRET_KEY, algorithm=seguridad.ALGORITMO,
        )
        for token in ("token-invalido", vencido):
            with self.subTest(token=token):
                self.assertEqual(
                    cliente.get("/auth/yo", headers={"Authorization": f"Bearer {token}"}).status_code,
                    401,
                )

    def test_openapi_declara_oauth2_solo_en_rutas_protegidas(self):
        esquema = cliente.get("/openapi.json").json()
        flujo = esquema["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"]["password"]
        self.assertEqual(flujo["tokenUrl"], "auth/login")
        for recurso in RECURSOS:
            rutas = esquema["paths"][recurso]
            self.assertNotIn("security", rutas["get"])
            self.assertIn("security", rutas["post"])


if __name__ == "__main__":
    unittest.main()
