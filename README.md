# API de la Tienda

Proyecto académico para la Guía 2 de APIs con FastAPI del programa Análisis y Desarrollo de Software (ADSO) del SENA. Es una API REST sencilla para administrar productos y categorías de una tienda virtual.

Los datos se guardan temporalmente en listas de Python; por eso se reinician cada vez que se detiene el servidor.

## Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic (incluido como dependencia de FastAPI)

## Estructura de carpetas

```text
tienda-api/
├── main.py
├── README.md
├── .gitignore
├── requirements.txt
├── routers/
│   ├── __init__.py
│   ├── productos.py
│   └── categorias.py
└── tests/
    └── test_api.py
```

## Funcionalidades

- Ruta principal para comprobar que la API funciona.
- CRUD completo de productos: listar, consultar, crear, actualizar y eliminar.
- CRUD completo de categorías: listar, consultar, crear, actualizar y eliminar.
- Validación automática de los datos mediante Pydantic.
- Respuesta `404` si un producto o una categoría no existen.
- Respuesta `422` si faltan campos obligatorios en una solicitud.

## Crear el entorno virtual

En la terminal, dentro de la carpeta `tienda-api`, ejecuta:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, usa este comando solo para la ventana actual y vuelve a activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Instalar FastAPI y Uvicorn

Con el entorno virtual activado, ejecuta:

```powershell
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` instala las dos dependencias necesarias: FastAPI y Uvicorn.

## Ejecutar el servidor

```powershell
python -m uvicorn main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`.

## Documentación interactiva

Abre `http://127.0.0.1:8000/docs` en el navegador. Allí se muestran todos los endpoints y se pueden probar con el botón **Try it out**.

## Endpoints principales

- `GET /`: comprueba que la API está funcionando.
- `GET`, `POST /productos`: lista o crea productos.
- `GET`, `PUT`, `DELETE /productos/{producto_id}`: consulta, actualiza o elimina un producto.
- `GET`, `POST /categorias`: lista o crea categorías.
- `GET`, `PUT`, `DELETE /categorias/{categoria_id}`: consulta, actualiza o elimina una categoría.

## Pruebas automatizadas opcionales

Con FastAPI instalado, puedes ejecutar las pruebas desde la carpeta del proyecto:

```powershell
python -m unittest discover -s tests
```
