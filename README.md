# Servidor FastAPI para Registro de Usuarios

Este servidor permite el registro de usuarios y está construido con FastAPI y sqlite. 

## Instalación

```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <REPOSITORIO>
```

## Crear entorno virtual y activalo

```bash
python -m venv venv
source venv/Scripts/activate  
```

## Instalar dependencias

Vamos a usar las siguientes bibliotecas:

- fastapi: Para construir la API.
- uvicorn: Como servidor ASGI para ejecutar la aplicación.
- sqlite3: Ya está incluido en Python, por lo que no necesitamos instalar nada adicional.
- pydantic: Para la validación de datos.

Puedes instalar las dependencias necesarias con:
```bash
pip install fastapi uvicorn pydantic
```

## Inicia el servidor

```bash
uvicorn app.main:app --reload
```

## Correr tests

```bash
pytest
```
