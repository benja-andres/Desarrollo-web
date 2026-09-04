const mongoose = require("mongoose");

async function conectarDB() {
  const uri = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/natural_power";

  try {
    await mongoose.connect(uri);
    console.log(`MongoDB conectado -> ${uri}`);
  } catch (error) {
    console.error("Error al conectar a MongoDB:", error.message);
    process.exit(1);
  }
}

module.exports = conectarDB;
