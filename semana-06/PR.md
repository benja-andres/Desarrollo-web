# Semana 06: API REST con FastAPI y MongoDB

## Resumen

Implementacion de una API REST con FastAPI, MongoDB y Motor para administrar items.

## Funcionalidades

- Endpoint de salud.
- CRUD completo de items.
- Modelos validados y conversion de ObjectId a id.
- Busqueda por nombre y paginacion.
- Errores 400, 404 y 422.
- Pruebas HTTP automatizadas con MongoDB simulado.

## Pruebas realizadas

```text
20 passed
```

## Como ejecutar

```powershell
python -m uvicorn main:app --reload
python -m pytest -q
```
