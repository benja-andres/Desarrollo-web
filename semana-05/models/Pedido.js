const mongoose = require("mongoose");

// Item embebido dentro del pedido. precioUnitario queda "congelado" al
// momento de la compra, para no depender de cambios futuros de precio.
const itemPedidoSchema = new mongoose.Schema(
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
    precioUnitario: {
      type: Number,
      required: true,
      min: 0,
    },
  },
  { _id: false }
);

const pedidoSchema = new mongoose.Schema(
  {
    usuarioId: {
      type: String,
      required: true,
      trim: true,
    },
    items: [itemPedidoSchema],
    total: {
      type: Number,
      required: true,
      min: 0,
    },
    estado: {
      type: String,
      enum: ["pendiente", "pagado", "enviado", "entregado", "cancelado"],
      default: "pendiente",
    },
    direccionEnvio: {
      type: String,
      trim: true,
    },
    metodoPago: {
      type: String,
      trim: true,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Pedido", pedidoSchema);
