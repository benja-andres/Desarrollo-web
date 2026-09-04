const mongoose = require("mongoose");

// Un combo agrupa varios productos (por ejemplo, jugo + smoothie) bajo un
// precio propio, tal como se muestra en la seccion "combos" del navbar.
const comboSchema = new mongoose.Schema(
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
    productos: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Producto",
      },
    ],
    activo: {
      type: Boolean,
      default: true,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Combo", comboSchema);
