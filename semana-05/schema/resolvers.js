const { UserInputError } = require("apollo-server-express");
const Producto = require("../models/Producto");
const Carrito = require("../models/Carrito");

// Un usuario tiene a lo más un carrito "abierto" a la vez; si no existe,
// se crea vacío la primera vez que agrega un ítem.
async function obtenerOCrearCarritoAbierto(usuarioId) {
  let carrito = await Carrito.findOne({ usuarioId, estado: "abierto" });
  if (!carrito) {
    carrito = await Carrito.create({ usuarioId, items: [] });
  }
  return carrito;
}

function poblarCarrito(query) {
  return query.populate("items.producto");
}

const resolvers = {
  Query: {
    productos: async () => {
      return Producto.find().sort({ createdAt: -1 });
    },
    producto: async (_, { id }) => {
      const producto = await Producto.findById(id);
      if (!producto) throw new UserInputError("Producto no encontrado");
      return producto;
    },
    productosDestacados: async () => {
      return Producto.find({ destacado: true }).sort({ createdAt: -1 });
    },

    carritoPorUsuario: async (_, { usuarioId }) => {
      return poblarCarrito(Carrito.findOne({ usuarioId, estado: "abierto" }));
    },
    carrito: async (_, { id }) => {
      const carrito = await poblarCarrito(Carrito.findById(id));
      if (!carrito) throw new UserInputError("Carrito no encontrado");
      return carrito;
    },
  },

  Mutation: {
    crearProducto: async (_, { input }) => {
      const producto = new Producto(input);
      return producto.save();
    },
    actualizarProducto: async (_, { id, input }) => {
      const producto = await Producto.findByIdAndUpdate(id, input, {
        new: true,
        runValidators: true,
      });
      if (!producto) throw new UserInputError("Producto no encontrado");
      return producto;
    },
    eliminarProducto: async (_, { id }) => {
      const resultado = await Producto.findByIdAndDelete(id);
      if (!resultado) throw new UserInputError("Producto no encontrado");
      return true;
    },

    agregarItemCarrito: async (_, { usuarioId, item }) => {
      const producto = await Producto.findById(item.productoId);
      if (!producto) throw new UserInputError("Producto no encontrado");

      const carrito = await obtenerOCrearCarritoAbierto(usuarioId);
      const itemExistente = carrito.items.find(
        (i) => i.producto.toString() === item.productoId
      );

      if (itemExistente) {
        itemExistente.cantidad += item.cantidad;
      } else {
        carrito.items.push({ producto: producto.id, cantidad: item.cantidad });
      }

      await carrito.save();
      return poblarCarrito(Carrito.findById(carrito.id));
    },

    actualizarItemCarrito: async (_, { usuarioId, productoId, cantidad }) => {
      const carrito = await Carrito.findOne({ usuarioId, estado: "abierto" });
      if (!carrito) throw new UserInputError("Carrito no encontrado");

      const item = carrito.items.find((i) => i.producto.toString() === productoId);
      if (!item) throw new UserInputError("El producto no esta en el carrito");

      if (cantidad <= 0) {
        carrito.items = carrito.items.filter(
          (i) => i.producto.toString() !== productoId
        );
      } else {
        item.cantidad = cantidad;
      }

      await carrito.save();
      return poblarCarrito(Carrito.findById(carrito.id));
    },

    eliminarItemCarrito: async (_, { usuarioId, productoId }) => {
      const carrito = await Carrito.findOne({ usuarioId, estado: "abierto" });
      if (!carrito) throw new UserInputError("Carrito no encontrado");

      carrito.items =  carrito.items.filter(
        (i) => i.producto.toString() !== productoId
      );

      await carrito.save();
      return poblarCarrito(Carrito.findById(carrito.id));
    },

    vaciarCarrito: async (_, { usuarioId }) => {
      const carrito = await Carrito.findOne({ usuarioId, estado: "abierto" });
      if (!carrito) throw new UserInputError("Carrito no encontrado");

      carrito.items = [];
      await carrito.save();
      return poblarCarrito(Carrito.findById(carrito.id));
    },
  },

  Carrito: {
    total: (carrito) =>
      carrito.items.reduce(
        (acc, item) => acc + item.producto.precio * item.cantidad,
        0
      ),
  },
  ItemCarrito: {
    subtotal: (item) => item.producto.precio * item.cantidad,
  },
};

module.exports = resolvers;