# Natural Power API

Backend GraphQL para el sitio de jugos y smoothies "Natural Power". Este
paquete incluye el setup completo del servidor (Express + Apollo Server +
Mongoose) y los modulos de **Productos y Combos** y **Carrito/Pedidos**,
correspondientes al reparto de entidades del trabajo en equipo.

## Stack

- Express + cors
- GraphQL 15.10.1 + Apollo Server Express 3.13.0
- Mongoose 8.17.1 (MongoDB)
- Nodemon para desarrollo

## Como correrlo

1. Instalar dependencias:

   ```bash
   npm install
   ```

2. Copiar `.env.example` a `.env` y ajustar la cadena de conexion a tu
   MongoDB (local con Compass/Community, o un cluster en la nube):

   ```bash
   cp .env.example .env
   ```

3. Levantar el servidor en modo desarrollo (con nodemon):

   ```bash
   npm start
   ```

4. Abrir el Sandbox de Apollo en `http://localhost:4000/graphql`.

## Estructura

```
natural-power-api/
├── config/
│   └── db.js              # Conexion a MongoDB
├── models/
│   ├── Producto.js         # Schema de Mongoose para productos
│   ├── Combo.js             # Schema de Mongoose para combos
│   ├── Carrito.js           # Schema de Mongoose para el carrito de compra
│   └── Pedido.js             # Schema de Mongoose para pedidos/ordenes
├── schema/
│   ├── typeDefs.js          # Tipos, Query y Mutation de GraphQL
│   └── resolvers.js         # Resolvers que consultan/persisten en Mongo
├── server.js                 # Punto de entrada (Express + Apollo)
├── .env.example
└── package.json
```

## Queries y Mutations disponibles

Query:

- `productos`
- `producto(id: ID!)`
- `productosDestacados`
- `combos`
- `combo(id: ID!)`
- `carritoPorUsuario(usuarioId: String!)`
- `carrito(id: ID!)`
- `pedidos`
- `pedido(id: ID!)`
- `pedidosPorUsuario(usuarioId: String!)`

Mutation:

- `crearProducto(input: ProductoInput!)`
- `actualizarProducto(id: ID!, input: ProductoUpdateInput!)`
- `eliminarProducto(id: ID!)`
- `crearCombo(input: ComboInput!)`
- `actualizarCombo(id: ID!, input: ComboUpdateInput!)`
- `eliminarCombo(id: ID!)`
- `agregarItemCarrito(usuarioId: String!, item: ItemCarritoInput!)`
- `actualizarItemCarrito(usuarioId: String!, productoId: ID!, cantidad: Int!)`
- `eliminarItemCarrito(usuarioId: String!, productoId: ID!)`
- `vaciarCarrito(usuarioId: String!)`
- `crearPedidoDesdeCarrito(usuarioId: String!, input: CrearPedidoInput)`
- `actualizarEstadoPedido(id: ID!, estado: String!)`
- `cancelarPedido(id: ID!)`

### Ejemplo: crear un producto

```graphql
mutation {
  crearProducto(
    input: {
      nombre: "Jugo Verde Detox"
      descripcion: "Espinaca, pepino, manzana verde y jengibre"
      precio: 3200
      imagen: "https://ejemplo.com/jugo-verde.jpg"
      categoria: "jugo"
      stock: 25
      destacado: true
    }
  ) {
    id
    nombre
    precio
  }
}
```

### Ejemplo: obtener productos destacados (home)

```graphql
query {
  productosDestacados {
    id
    nombre
    descripcion
    precio
    imagen
  }
}
```

### Ejemplo: agregar un item al carrito

```graphql
mutation {
  agregarItemCarrito(
    usuarioId: "gabriel@example.com"
    item: { productoId: "665f1a2b3c4d5e6f7a8b9c0d", cantidad: 2 }
  ) {
    id
    total
    items {
      cantidad
      subtotal
      producto {
        nombre
        precio
      }
    }
  }
}
```

### Ejemplo: hacer checkout del carrito (crear pedido)

```graphql
mutation {
  crearPedidoDesdeCarrito(
    usuarioId: "gabriel@example.com"
    input: { direccionEnvio: "Av. Siempre Viva 123", metodoPago: "webpay" }
  ) {
    id
    total
    estado
    items {
      cantidad
      precioUnitario
      subtotal
    }
  }
}
```

El carrito solo se puede convertir en pedido si tiene items; al hacerlo,
el precio de cada producto queda "congelado" en `precioUnitario` y el
carrito pasa a estado `cerrado` (queda como historial). El siguiente item
que el usuario agregue abre un carrito nuevo automáticamente.

## Integrando el resto del equipo

Cada compañero agrega su propia carpeta de modelo y sus propios `typeDefs`
y `resolvers` (por ejemplo `Usuario`). Para unir todo, basta con:

1. Agregar el nuevo archivo de tipos en `schema/typeDefs.js` (o crear un
   archivo separado y combinarlo con `mergeTypeDefs` de `@graphql-tools/merge`).
2. Agregar los resolvers correspondientes en `schema/resolvers.js` (o
   combinarlos con `mergeResolvers`).
3. No es necesario tocar `server.js` ni `config/db.js`: ya quedan listos
   para todo el equipo.
