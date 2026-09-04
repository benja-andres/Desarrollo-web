const mongoose = require("mongoose");

// Coincide con las tarjetas "producto" del wireframe:
// imagen, descripcion, precio y boton "añadir" (se resuelve en el front),
// mas categoria/stock/destacado para soportar "productos destacados" del home.
const productoSchema = new mongoose.Schema(
  {
    nombre: {
      type: String,
      required: true,
      trim: true,
    },
    descripcion: {
      type: String,
      required: true,
      trim: true,
    },
    precio: {
      type: Number,
      required: true,
      min: 0,
    },
    imagen: {
      type: String,
      required: true,
    },
    categoria: {
      type: String,
      enum: ["jugo", "smoothie", "otro"],
      default: "otro",
    },
    stock: {
      type: Number,
      default: 0,
      min: 0,
    },
    destacado: {
      type: Boolean,
      default: false,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Producto", productoSchema);
