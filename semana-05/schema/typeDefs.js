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

  input ItemCarritoInput {
    productoId: ID!
    cantidad: Int!
  }

  type Query {
    productos: [Producto!]!
    producto(id: ID!): Producto
    productosDestacados: [Producto!]!

    carritoPorUsuario(usuarioId: String!): Carrito
    carrito(id: ID!): Carrito
  }

  type Mutation {
    crearProducto(input: ProductoInput!): Producto!
    actualizarProducto(id: ID!, input: ProductoUpdateInput!): Producto!
    eliminarProducto(id: ID!): Boolean!

    agregarItemCarrito(usuarioId: String!, item: ItemCarritoInput!): Carrito!
    actualizarItemCarrito(
      usuarioId: String!
      productoId: ID!
      cantidad: Int!
    ): Carrito!
    eliminarItemCarrito(usuarioId: String!, productoId: ID!): Carrito!
    vaciarCarrito(usuarioId: String!): Carrito!
  }
`;

module.exports = typeDefs;