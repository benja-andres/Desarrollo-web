# Avance Unidad 2: Modelado C4 en Structurizr DSL - Natural Power

Este directorio contiene la especificación formal de arquitectura del backend seguro de
**Natural Power**, correspondiente a la Evaluación de la Unidad 2. El modelo describe el
backend tal como está implementado en `natural-power-backend/` (puertos, servicios y
relaciones verificados contra el código).

## 1. Niveles modelados

1. **Nivel C1 - Contexto del sistema (`C1_Contexto`)**
   - Actores: *Visitante* (anónimo), *Cliente* (autenticado) y *Operador / Admin*.
   - Sistema principal: *Plataforma Comercial Natural Power*.
   - Dependencia externa: *Plataforma de Pagos* (en el proyecto la simula `provider-mock`).

2. **Nivel C2 - Contenedores (`C2_Contenedores`)**
   - **Frontend Responsivo** (navegador web; sus contratos vienen de la Unidad 1).
   - **API Gateway** (único punto de entrada HTTP, puerto 8080) y **GraphQL Gateway** (agregador privado).
   - **Auth Service** (JWT, sesiones) y **Secret Manager** (secretos por referencia simbólica con ACL).
   - **Servicios privados:** `inventory`, `orders`, `clients` y `payments`.
   - **Persistencia:** una base SQLite por servicio (`dbIdentity`, `dbInventory`, `dbOrders`, `dbClients`, `dbPayments`).

3. **Nivel C3 - Componentes internos**
   - **API Gateway (`C3_ApiGateway`):** HTTP Adapter, Access Filter, Route Dispatcher y Error Mapper.
   - **Auth Service (`C3_Auth`):** API Identidad, Gestor de Sesiones, Verificador de Credenciales, Cliente de Secretos y Repositorio de Identidades.
   - **GraphQL Gateway (`C3_GraphQL`):** Endpoint GraphQL, Validador de Consultas, Política de Acceso a Campos, Resolvers, Conectores de Subsistemas y Compositor de Respuestas.
   - **Orders Service (`C3_Orders`):** API Pedidos, Política de Acceso (anti-IDOR), Control de Idempotencia, Servicio de Pedidos, Adaptadores Inventory/Payments y Repositorio de Pedidos.

4. **Vistas dinámicas**
   - `Dyn_Catalogo`: consulta de catálogo por un visitante.
   - `Dyn_Compra`: crear pedido, reservar stock, pagar con webhook firmado y marcar el pedido como pagado.

## 2. Cómo visualizar los diagramas

1. Abrir [Structurizr Playground](https://playground.structurizr.com/) o [structurizr.com/dsl](https://structurizr.com/dsl).
2. Copiar y pegar el contenido de `workspace.dsl`.
3. Cambiar entre las vistas `C1_Contexto`, `C2_Contenedores`, `C3_ApiGateway`, `C3_Auth`, `C3_GraphQL`, `C3_Orders`, `Dyn_Catalogo` y `Dyn_Compra`.

Las exportaciones PNG de cada vista están en `diagramas/`.

## 3. Archivos

- `workspace.dsl`: especificación en Structurizr DSL.
- `README.md`: este documento.
- `diagramas/`: exportaciones PNG de las vistas.
