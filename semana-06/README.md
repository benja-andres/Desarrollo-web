# Semana 06 - FastAPI + MongoDB

API REST para crear, listar, consultar, actualizar y eliminar items.

## Ejecucion

Instalar las dependencias de `requirements.txt` y `requirements-dev.txt`, iniciar
MongoDB con Docker Compose y ejecutar:

```powershell
python -m uvicorn main:app --reload
```

Documentacion: `http://127.0.0.1:8000/docs`

## Rutas

- `GET /health`
- `GET /items`
- `POST /items`
- `GET /items/{item_id}`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`
