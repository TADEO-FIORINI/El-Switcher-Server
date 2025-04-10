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

## Extra

El servidor actualmente esta corriendo en Render. Utilizo el plan gratuito con 512 Mb (RAM). 
Ademas, los servidores de Render se encuentran en EEUU. 
Por esto, tenemos una latencia de 1 a 2 segundos.

En el plan gratuito de Render, el servidor entra en estado "sleep" si no recibe una solicitus en un determinado tiempo (15 minutos aprox.), lo que causa que la proxima solicitud tarde mucho mas, ya que tiene que despertar la instancia del servidor.

Para evitar que el servidor entre en modo sleep, configuramos un servicio externo, Uptimerobot, para que llame a la api "ping" cada 5 minutos y evitar que el servidor entre en modo sleep en Render.

