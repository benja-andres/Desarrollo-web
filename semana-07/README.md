# Laboratorio API Gateway (FastAPI + HTTPX)

Pasos 1 a 3 de la guía "API Gateway local con FastAPI y HashiCorp Vault".

```
Cliente --> API Gateway :8000 (HOST A) --> Backend API :9000 (HOST B)
```

| Carpeta        | Contenido                | Host   | Puerto |
|----------------|--------------------------|--------|--------|
| `backend-api/` | API REST de negocio      | HOST B | 9000   |
| `api-gateway/` | API Gateway básico       | HOST A | 8000   |

Cada carpeta tiene su propio `README.md` y `requirements.txt`.
