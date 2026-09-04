const { UserInputError } = require("apollo-server-express");
const Producto = require("../models/Producto");
const Combo = require("../models/Combo");
const Carrito = require("../models/Carrito");
const Pedido = require("../models/Pedido");

const ESTADOS_PEDIDO = ["pendiente", "pagado", "enviado", "entregado", "cancelado"];

// Un usuario tiene a lo mas un carrito "abierto" a la vez; si no existe,
// se crea vacio la primera vez que agrega un item.
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

function poblarPedido(query) {
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
    combos: async () => {
      return Combo.find().populate("productos").sort({ createdAt: -1 });
    },
    combo: async (_, { id }) => {
      const combo = await Combo.findById(id).populate("productos");
      if (!combo) throw new UserInputError("Combo no encontrado");
      return combo;
    },

    carritoPorUsuario: async (_, { usuarioId }) => {
      return poblarCarrito(Carrito.findOne({ usuarioId, estado: "abierto" }));
    },
    carrito: async (_, { id }) => {
      const carrito = await poblarCarrito(Carrito.findById(id));
      if (!carrito) throw new UserInputError("Carrito no encontrado");
      return carrito;
    },

    pedidos: async () => {
      return poblarPedido(Pedido.find().sort({ createdAt: -1 }));
    },
    pedido: async (_, { id }) => {
      const pedido = await poblarPedido(Pedido.findById(id));
      if (!pedido) throw new UserInputError("Pedido no encontrado");
      return pedido;
    },
    pedidosPorUsuario: async (_, { usuarioId }) => {
      return poblarPedido(Pedido.find({ usuarioId }).sort({ createdAt: -1 }));
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

    crearCombo: async (_, { input }) => {
      const combo = new Combo(input);
      await combo.save();
      return combo.populate("productos");
    },
    actualizarCombo: async (_, { id, input }) => {
      const combo = await Combo.findByIdAndUpdate(id, input, {
        new: true,
        runValidators: true,
      }).populate("productos");
      if (!combo) throw new UserInputError("Combo no encontrado");
      return combo;
    },
    eliminarCombo: async (_, { id }) => {
      const resultado = await Combo.findByIdAndDelete(id);
      if (!resultado) throw new UserInputError("Combo no encontrado");
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

      carrito.items = carrito.items.filter(
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

    crearPedidoDesdeCarrito: async (_, { usuarioId, input }) => {
      const carrito = await poblarCarrito(
        Carrito.findOne({ usuarioId, estado: "abierto" })
      );
      if (!carrito || carrito.items.length === 0) {
        throw new UserInputError("El carrito esta vacio o no existe");
      }

      const items = carrito.items.map((item) => ({
        producto: item.producto.id,
        cantidad: item.cantidad,
        precioUnitario: item.producto.precio,
      }));
      const total = items.reduce(
        (acc, item) => acc + item.precioUnitario * item.cantidad,
        0
      );

      const pedido = await Pedido.create({
        usuarioId,
        items,
        total,
        direccionEnvio: input?.direccionEnvio,
        metodoPago: input?.metodoPago,
      });

      // El carrito queda como historial y se cierra; el proximo item que
      // agregue el usuario abrira uno nuevo automaticamente.
      carrito.estado = "cerrado";
      await carrito.save();

      return poblarPedido(Pedido.findById(pedido.id));
    },

    actualizarEstadoPedido: async (_, { id, estado }) => {
      if (!ESTADOS_PEDIDO.includes(estado)) {
        throw new UserInputError(
          `Estado invalido. Debe ser uno de: ${ESTADOS_PEDIDO.join(", ")}`
        );
      }

      const pedido = await poblarPedido(
        Pedido.findByIdAndUpdate(id, { estado }, { new: true })
      );
      if (!pedido) throw new UserInputError("Pedido no encontrado");
      return pedido;
    },

    cancelarPedido: async (_, { id }) => {
      const pedido = await poblarPedido(
        Pedido.findByIdAndUpdate(id, { estado: "cancelado" }, { new: true })
      );
      if (!pedido) throw new UserInputError("Pedido no encontrado");
      return pedido;
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
  ItemPedido: {
    subtotal: (item) => item.precioUnitario * item.cantidad,
  },
};

module.exports = resolvers;
