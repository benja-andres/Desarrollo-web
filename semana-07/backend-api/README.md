# Backend API (Paso 2, HOST B)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
```bash
uvicorn backend_api:app --host 0.0.0.0 --port 9000
```
```bash
curl http://localhost:9000/health
curl http://localhost:9000/products
curl http://localhost:9000/orders
```
