# Semana 08: API Gateway seguro con FastAPI y HashiCorp Vault

Guía práctica para construir un Gateway que autentica clientes, obtiene secretos de Vault y reenvía solicitudes a una API de negocio protegida en otro host.

## Propósito del laboratorio

El cliente no accede directamente a la API de negocio: todas las solicitudes pasan primero por el API Gateway, que valida la identidad del cliente y sólo entonces enruta la operación al backend. Al finalizar, se debe poder explicar la diferencia entre autenticación, autorización, gestión de secretos y aislamiento de red.

## Objetivos

- Crear una API REST con FastAPI en un segundo host.
- Proteger la API de negocio con una credencial interna.
- Levantar HashiCorp Vault y almacenar credenciales fuera del código.
- Validar Bearer Tokens en un API Gateway.
- Enrutar solicitudes autorizadas al backend y probar casos de error.

## Arquitectura y puertos

| Componente | Host de ejemplo | Puerto | Responsabilidad |
|---|---|---:|---|
| API Gateway | HOST A `192.168.1.10` | 8000 | Autenticar y enrutar solicitudes |
| HashiCorp Vault | HOST A | 8200 | Almacenar secretos del laboratorio |
| Backend API | HOST B `192.168.1.20` | 9000 | Servir productos y pedidos |

```text
Cliente -- Authorization: Bearer ... --> Gateway -- X-Gateway-Secret --> Backend
                                           |
                                           +---- lee secretos ----> Vault
```

Las direcciones IP son ejemplos. Sustitúyelas por las direcciones reales de los equipos. Ambos hosts deben tener Python 3.11 o superior y conectividad de red. HOST A necesita Docker.

## 1. Comprobar la conectividad

Desde HOST A:

```powershell
ping 192.168.1.20
```

Desde HOST B:

```powershell
ping 192.168.1.10
```

Si no hay respuesta, revisar la configuración de red de las máquinas virtuales y las reglas de firewall.

## 2. Crear y ejecutar el backend (HOST B)

Copiar la carpeta `gabo/backend-api` a HOST B, abrir una terminal en ella y crear el entorno:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En PowerShell, configurar el secreto interno del laboratorio (debe coincidir con el valor guardado en Vault):

```powershell
$env:INTERNAL_GATEWAY_SECRET="gateway-api-secret-456"
```

En Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
export INTERNAL_GATEWAY_SECRET="gateway-api-secret-456"
```

Iniciar la API:

```bash
uvicorn backend_api:app --host 0.0.0.0 --port 9000
```

El backend entrega `GET /health`, `GET /products` y `GET /orders`. Los endpoints de negocio requieren `X-Gateway-Secret`; `/health` queda disponible para comprobar el servicio.

## 3. Verificar el rechazo de una llamada directa

Desde un equipo que alcance a HOST B, llamar al backend sin secreto:

```bash
curl -i http://192.168.1.20:9000/products
```

Resultado esperado: `403 Forbidden`. Para confirmar que el backend responde con el secreto correcto:

```bash
curl -i -H "X-Gateway-Secret: gateway-api-secret-456" http://192.168.1.20:9000/products
```

## 4. Iniciar Vault en HOST A

Para este laboratorio se utiliza Vault en modo de desarrollo. En HOST A:

```bash
docker run --name vault-dev -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=dev-only-token -d hashicorp/vault
```

Este modo y el token raíz son exclusivamente educativos; no se deben usar en producción. Guardar los dos secretos de ejemplo en el motor KV:

```bash
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put secret/gateway client_token="student-token-123" backend_shared_secret="gateway-api-secret-456"
```

Comprobar que se guardaron:

```bash
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv get secret/gateway
```

`client_token` autentica al cliente frente al Gateway. `backend_shared_secret` autentica al Gateway frente al backend. Son identidades distintas.

## 5. Configurar y ejecutar el Gateway (HOST A)

Copiar `benjamin/api-gateway` a HOST A y preparar el entorno:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configurar las variables en PowerShell:

```powershell
$env:VAULT_ADDR="http://127.0.0.1:8200"
$env:VAULT_TOKEN="dev-only-token"
$env:BACKEND_URL="http://192.168.1.20:9000"
```

En Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="dev-only-token"
export BACKEND_URL="http://192.168.1.20:9000"
```

Iniciar el Gateway:

```bash
uvicorn gateway:app --host 0.0.0.0 --port 8000
```

El Gateway expone `GET /health` y recibe solicitudes en `/api/{ruta}`. El proxy reenvía los métodos GET, POST, PUT, PATCH y DELETE, junto con el cuerpo y los parámetros de consulta.

## 6. Probar el flujo de autenticación

Reemplazar `192.168.1.10` por la IP de HOST A.

Sin token (esperado: `401`):

```bash
curl -i http://192.168.1.10:8000/api/products
```

Con token incorrecto (esperado: `401`):

```bash
curl -i -H "Authorization: Bearer token-incorrecto" http://192.168.1.10:8000/api/products
```

Con token válido (esperado: `200` y la lista de productos):

```bash
curl -i -H "Authorization: Bearer student-token-123" http://192.168.1.10:8000/api/products
```

También se puede probar la ruta de pedidos:

```bash
curl -i -H "Authorization: Bearer student-token-123" http://192.168.1.10:8000/api/orders
```

## 7. Rotar el token

En HOST A, escribir otro `client_token` en Vault manteniendo el secreto interno:

```bash
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put secret/gateway client_token="nuevo-token-789" backend_shared_secret="gateway-api-secret-456"
```

Probar otra vez con `student-token-123`: debe responder `401`. El nuevo token `nuevo-token-789` debe permitir la solicitud. No hace falta modificar el código del Gateway.

## 8. Matriz de resultados esperados

| Prueba | Resultado |
|---|---|
| Gateway sin token | `401 Unauthorized` |
| Gateway con token inválido | `401 Unauthorized` |
| Gateway con token válido y backend disponible | `200 OK` |
| Acceso directo al backend sin secreto | `403 Forbidden` |
| Vault inaccesible o secreto no disponible | `500` controlado |
| Backend inaccesible | `502 Bad Gateway` |
| Token rotado: token anterior / token nuevo | `401` / acceso exitoso |

### Ejecutar pruebas automatizadas locales

Desde la carpeta `semana-08`, instalar las dependencias de ambas aplicaciones y ejecutar:

```bash
python -m pip install -r gabo/backend-api/requirements.txt
python -m pip install -r benjamin/api-gateway/requirements.txt
python -m unittest discover -s gabo/tests -v
```

Estas pruebas no requieren iniciar Vault ni conectar dos equipos: simulan la respuesta de Vault y del backend, y verifican autenticación, rechazo de acceso directo, reenvío, rotación del token y respuestas controladas `500`/`502`. La matriz anterior describe además las verificaciones manuales de integración.

### Resultado de ejecución integrada local

Se levantó Vault real en Docker y se ejecutaron el backend y el Gateway como procesos locales, usando `127.0.0.1` para representar HOST A y HOST B:

| Escenario ejecutado | Resultado |
|---|---|
| Backend directo sin secreto interno | `403` |
| Backend directo con secreto correcto | `200` |
| Secreto interno incorrecto entre Gateway y backend | `403` |
| Gateway sin Bearer Token | `401` |
| Gateway con token inválido | `401` |
| Gateway con token válido a `/products` y `/orders` | `200` |
| Rotación de token en Vault (token anterior / nuevo) | `401` / `200` |
| Vault detenido temporalmente | `500` |
| Backend detenido temporalmente | `502` |

La conectividad entre dos equipos y las reglas de firewall requieren el laboratorio en hosts separados; no se validaron en esta ejecución local.

## 9. Flujo completo

1. El cliente envía `Authorization: Bearer <token>` al Gateway.
2. El Gateway consulta Vault y obtiene el token esperado y el secreto interno.
3. El Gateway compara el token recibido de forma segura; si no coincide, responde `401`.
4. Si coincide, el Gateway envía la solicitud al backend incluyendo `X-Gateway-Secret`.
5. El backend verifica el secreto y procesa la operación; si falta o es incorrecto, responde `403`.
6. El Gateway devuelve al cliente el estado y el cuerpo de la respuesta del backend.

En síntesis: `Solicitud → Autenticación → Autorización → Enrutamiento → Backend`.

## 10. Relación con conceptos de Arquitectura de Software

| Elemento | Aplicación en el laboratorio |
|---|---|
| Concern | Seguridad de acceso a APIs y protección de credenciales |
| Decisiones | Centralizar el control en el Gateway, externalizar secretos, separar identidades y proteger el backend |
| Mecanismos | Bearer Token, HashiCorp Vault, dependencias de FastAPI, HTTPX y secreto interno entre servicios |
| Evidencia | Respuestas HTTP `401`, `403`, `500` y `502`; comportamiento después de rotar un secreto |

### Autenticación y autorización

- **Autenticación:** responde “¿quién eres?”. En esta práctica, el cliente debe presentar un Bearer Token válido.
- **Autorización:** responde “¿qué puedes hacer?”. En el ejemplo, cualquier cliente con token válido accede a los endpoints protegidos. No hay roles implementados todavía.
- **Gestión de secretos:** guarda credenciales fuera del código, en Vault.
- **Aislamiento de red:** limita qué equipos pueden conectarse al backend; complementa, pero no reemplaza, la validación de aplicación.

## 11. Extensión: roles y scopes

Como actividad, extender la autorización para tener dos perfiles:

- `usuario`: sólo puede ejecutar `GET /products`.
- `administrador`: puede acceder a `/products` y `/orders`.

Una posible política sería `usuario → products:read` y `administrador → products:read, orders:read`. La decisión puede tomarse en el Gateway a partir de la identidad asociada al token. Si el token no existe o es incorrecto, responder `401`; si es válido pero no permite la operación, responder `403`.

## 12. Preguntas para discusión

1. ¿Qué aporta el API Gateway que no resuelva directamente la API de negocio?
2. ¿Por qué conviene guardar tokens y contraseñas fuera del código fuente?
3. ¿En qué se diferencian el token del cliente y el secreto Gateway–Backend?
4. ¿Qué riesgo aparece si alguien accede directamente al backend?
5. ¿Por qué hace falta firewall aunque el backend valide un secreto?
6. ¿Qué riesgo tiene compartir un único token entre todos los clientes?
7. ¿Qué ventajas y costos tendría reemplazar este token por JWT?
8. ¿Qué componentes cambiarían al delegar la autenticación a un Identity Provider?

## 13. Limitaciones

Esta implementación es didáctica y no constituye una arquitectura lista para producción. Vault se ejecuta en modo dev y se usa un token estático de laboratorio. En un entorno real se deben considerar, entre otros, OAuth 2.0/OpenID Connect o un Identity Provider, credenciales de Vault de privilegio mínimo, expiración y renovación de secretos, HTTPS/mTLS, segmentación de red, rate limiting, logging estructurado, monitoreo y políticas de autorización más completas.

## 14. Red y consideraciones de seguridad

Además de validar la credencial interna, restringir en el firewall de HOST B el puerto TCP 9000 para que sólo acepte conexiones desde la IP de HOST A. En Linux con UFW, por ejemplo:

```bash
sudo ufw insert 1 allow from 192.168.1.10 to any port 9000 proto tcp
```

Un header HTTP por sí solo no reemplaza el aislamiento de red ni TLS. Para un sistema real se deben usar secretos con privilegios mínimos, HTTPS/mTLS, autenticación y autorización apropiadas, y una configuración de Vault distinta del modo dev.

## 15. Actividad de cierre

Implementar los perfiles definidos en la sección de extensión y documentar: qué información se almacena en Vault, dónde se toma la decisión de autorización, qué identidad se comunica al backend y qué código HTTP corresponde a cada escenario. La respuesta debe distinguir claramente `401` (no autenticado) de `403` (autenticado, pero sin permiso).
