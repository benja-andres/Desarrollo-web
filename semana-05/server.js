require("dotenv").config();

const express = require("express");
const cors = require("cors");
const { ApolloServer } = require("apollo-server-express");

const conectarDB = require("./config/db");
const typeDefs = require("./schema/typeDefs");
const resolvers = require("./schema/resolvers");

async function iniciarServidor() {
  // 1. Conexion a la base de datos
  await conectarDB();

  // 2. Servidor Express base
  const app = express();
  app.use(cors());

  // 3. Servidor Apollo (capa GraphQL) montado sobre Express
  const apolloServer = new ApolloServer({
    typeDefs,
    resolvers,
  });
  await apolloServer.start();
  apolloServer.applyMiddleware({ app, path: "/graphql" });

  const PORT = process.env.PORT || 4000;
  app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
    console.log(
      `Sandbox de GraphQL disponible en http://localhost:${PORT}${apolloServer.graphqlPath}`
    );
  });
}

iniciarServidor().catch((error) => {
  console.error("Error al iniciar el servidor:", error);
  process.exit(1);
});
