# API Gateway básico (Paso 3, HOST A)

Requiere el backend corriendo (ver `../backend-api`).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Con dos hosts, apuntar al backend (por defecto `http://localhost:9000`):
```powershell
$env:BACKEND_URL = "http://192.168.1.20:9000"
```
```bash
uvicorn gateway:app --host 0.0.0.0 --port 8000
```
```bash
curl http://localhost:8000/api/products
curl http://localhost:8000/api/orders
```
