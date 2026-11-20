# API de la Tienda

Proyecto académico de la Guía 3 de FastAPI del programa Análisis y Desarrollo de Software (ADSO) del SENA. Continúa la API de la Guía 2 y agrega inicio de sesión con JWT, hashing de contraseñas con bcrypt y permisos según el rol.

## Ejecutar el proyecto

Requiere Python 3.10 o superior. En PowerShell, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

En Ubuntu o WSL:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

Abre [Swagger UI](http://127.0.0.1:8000/docs). Para probar una ruta, selecciona **Try it out** y luego **Execute**. Usa **Authorize** para cambiar de cuenta y **Logout** para volver a probar sin token.

| Usuario de prueba | Contraseña | Rol |
| --- | --- | --- |
| ana | ana123 | cliente |
| admin | admin123 | admin |

## Rutas y permisos

| Petición | Acceso | Estado de éxito |
| --- | --- | --- |
| GET / | Público | 200 |
| POST /auth/login | Público. Recibe username y password como formulario | 200 |
| POST /auth/registro | Público. Recibe username, nombre y password como JSON y asigna el rol cliente | 201 |
| GET /auth/yo | Cualquier cuenta con JWT válido | 200 |
| GET de colección o por ID | Público | 200 |
| POST de colección | Cualquier cuenta con JWT válido | 201 |
| PUT por ID | Cualquier cuenta con JWT válido | 200 |
| DELETE por ID | Rol admin | 200 |

El CRUD aplica a `/productos`, `/categorias`, `/marcas` y `/proveedores`. Marcas y proveedores son los dos recursos adicionales incorporados a esta versión. El repositorio base contenía productos y categorías.

Productos recibe `nombre`, `precio` y `categoria`. Categorías, marcas y proveedores reciben `nombre`. El servidor crea el ID. La respuesta al crear un producto también incluye `creado_por`.

## Prueba rápida

1. Ejecuta `GET /productos` antes de iniciar sesión. Devuelve 200.
2. Intenta `POST /productos` con `{"nombre":"Webcam HD","precio":150000,"categoria":"Perifericos"}` sin iniciar sesión. Devuelve 401.
3. En **Authorize**, entra como Ana y repite el POST. Devuelve 201 y `creado_por: ana`. Prueba PUT con el ID devuelto.
4. Intenta borrar ese ID como Ana. Devuelve 403. Entra como admin y repite DELETE. Devuelve 200.
5. En `POST /auth/registro`, envía `{"username":"sofia","nombre":"Sofía Demo","password":"sofia123"}`. Inicia sesión con esa cuenta y consulta `GET /auth/yo`.
6. Repite los permisos en categorías, marcas y proveedores con un cuerpo como `{"nombre":"Ejemplo"}`.

## Organización y alcance

`seguridad.py` guarda los hashes de las contraseñas de prueba y define la firma, la validación de tokens y las dependencias de acceso. `routers/auth.py` reúne el login, el registro y la consulta de la cuenta actual. Cada CRUD tiene su router, y `main.py` los conecta.

Los JWT contienen el identificador del usuario y caducan a los 30 minutos. La cabecera es `Authorization: Bearer <token>`. Un token ausente, inválido o vencido devuelve 401. Una cuenta autenticada sin el rol necesario recibe 403.

Los datos viven en memoria y se reinician junto con el servidor. Las dos cuentas iniciales son para el laboratorio. Cuando no se configura `JWT_SECRET_KEY`, se genera una clave temporal al iniciar el proceso.

## Pruebas automatizadas

En la carpeta del proyecto, instala `requirements-dev.txt` y ejecuta `python -m unittest discover -s tests -v` con el intérprete del entorno virtual. Las pruebas verifican las rutas HTTP, el registro, los permisos, el inicio de sesión fallido y el rechazo de tokens inválidos o vencidos.

## Evidencias de la Guía 3

En `evidencias/guia3/` se encuentran los cuatro documentos de entrega y las capturas originales de respuesta. EV01 contiene la reflexión, EV02 el mapa conceptual y el flujo, EV03 la práctica con productos y autenticación, y EV04 los permisos de categorías y los dos recursos adicionales.

Las capturas corresponden a Swagger UI con respuestas reales de la aplicación mediante TestClient en un entorno de prueba automatizado. Los tokens y el comando de reproducción quedan fuera del recorte. Se verificaron 34 respuestas en Swagger y las pruebas de `tests/test_api.py` pasaron.

Los recursos adicionales elegidos son marcas y proveedores porque el repositorio de la Guía 2 solo contenía productos y categorías. Si los recursos de la sesión presencial tenían otros nombres, esos dos deben ajustarse a la versión de clase.
