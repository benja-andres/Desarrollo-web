const { gql } = require("apollo-server-express");

const typeDefs = gql`
  type Producto {
    id: ID!
    nombre: String!
    descripcion: String!
    precio: Float!
    imagen: String!
    categoria: String!
    stock: Int!
    destacado: Boolean!
    createdAt: String
    updatedAt: String
  }

  type Combo {
    id: ID!
    nombre: String!
    descripcion: String!
    precio: Float!
    imagen: String!
    productos: [Producto!]!
    activo: Boolean!
    createdAt: String
    updatedAt: String
  }

  input ProductoInput {
    nombre: String!
    descripcion: String!
    precio: Float!
    imagen: String!
    categoria: String
    stock: Int
    destacado: Boolean
  }

  input ProductoUpdateInput {
    nombre: String
    descripcion: String
    precio: Float
    imagen: String
    categoria: String
    stock: Int
    destacado: Boolean
  }

  input ComboInput {
    nombre: String!
    descripcion: String!
    precio: Float!
    imagen: String!
    productos: [ID!]
    activo: Boolean
  }

  input ComboUpdateInput {
    nombre: String
    descripcion: String
    precio: Float
    imagen: String
    productos: [ID!]
    activo: Boolean
  }

  type ItemCarrito {
    producto: Producto!
    cantidad: Int!
    subtotal: Float!
  }

  type Carrito {
    id: ID!
    usuarioId: String!
    items: [ItemCarrito!]!
    estado: String!
    total: Float!
    createdAt: String
    updatedAt: String
  }

  type ItemPedido {
    producto: Producto!
    cantidad: Int!
    precioUnitario: Float!
    subtotal: Float!
  }

  type Pedido {
    id: ID!
    usuarioId: String!
    items: [ItemPedido!]!
    total: Float!
    estado: String!
    direccionEnvio: String
    metodoPago: String
    createdAt: String
    updatedAt: String
  }

  input ItemCarritoInput {
    productoId: ID!
    cantidad: Int!
  }

  input CrearPedidoInput {
    direccionEnvio: String
    metodoPago: String
  }

  type Query {
    productos: [Producto!]!
    producto(id: ID!): Producto
    productosDestacados: [Producto!]!
    combos: [Combo!]!
    combo(id: ID!): Combo

    carritoPorUsuario(usuarioId: String!): Carrito
    carrito(id: ID!): Carrito

    pedidos: [Pedido!]!
    pedido(id: ID!): Pedido
    pedidosPorUsuario(usuarioId: String!): [Pedido!]!
  }

  type Mutation {
    crearProducto(input: ProductoInput!): Producto!
    actualizarProducto(id: ID!, input: ProductoUpdateInput!): Producto!
    eliminarProducto(id: ID!): Boolean!

    crearCombo(input: ComboInput!): Combo!
    actualizarCombo(id: ID!, input: ComboUpdateInput!): Combo!
    eliminarCombo(id: ID!): Boolean!

    agregarItemCarrito(usuarioId: String!, item: ItemCarritoInput!): Carrito!
    actualizarItemCarrito(
      usuarioId: String!
      productoId: ID!
      cantidad: Int!
    ): Carrito!
    eliminarItemCarrito(usuarioId: String!, productoId: ID!): Carrito!
    vaciarCarrito(usuarioId: String!): Carrito!

    crearPedidoDesdeCarrito(
      usuarioId: String!
      input: CrearPedidoInput
    ): Pedido!
    actualizarEstadoPedido(id: ID!, estado: String!): Pedido!
    cancelarPedido(id: ID!): Pedido!
  }
`;

module.exports = typeDefs;
