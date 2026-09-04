const mongoose = require("mongoose");

// Item embebido dentro del carrito: referencia al producto + cantidad.
const itemCarritoSchema = new mongoose.Schema(
  {
    producto: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Producto",
      required: true,
    },
    cantidad: {
      type: Number,
      required: true,
      min: 1,
    },
  },
  { _id: false }
);

// Un carrito "abierto" por usuario mientras compra; al hacer checkout se
// convierte en Pedido y el carrito pasa a "cerrado" (queda como historial).
const carritoSchema = new mongoose.Schema(
  {
    usuarioId: {
      type: String,
      required: true,
      trim: true,
    },
    items: [itemCarritoSchema],
    estado: {
      type: String,
      enum: ["abierto", "cerrado"],
      default: "abierto",
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Carrito", carritoSchema);
