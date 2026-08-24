<!DOCTYPE html>
<html lang="es">
<head>
  
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <title>Página Principal</title>
</head>
<body>


<nav class="navbar navbar-expand-sm navbar-dark" style="background-color: #3E2010;">
  <div class="container-fluid">

    <a class="navbar-brand fw-bold text-white" href="index.php">
      MonkeyStore
    </a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="menu">

      <ul class="navbar-nav me-auto">

        <li class="nav-item">
          <a class="nav-link fw-bold text-white" href="index.php">Principal</a>
        </li>

        <li class="nav-item">
          <a class="nav-link fw-bold text-white" href="empresa.php">Empresa</a>
        </li>

        <li class="nav-item">
          <a class="nav-link fw-bold text-white" href="productos.php">Productos</a>
        </li>

        <li class="nav-item">
          <a class="nav-link fw-bold text-white" href="galeria.php">Galería</a>
        </li>

        <li class="nav-item">
          <a class="nav-link fw-bold text-white" href="contacto.php">Contacto</a>
        </li>

      </ul>

      <a class="btn btn-success fw-bold border border-2 border-white" href="acceso.php">
        Acceder
      </a>

    </div>
  </div>
</nav>


<div class="container-fluid" style="background-color: #fEfAEE;">
  <h4>Página Principal</h4>
  <p><a href="index.php">Ir a Principal</a></p>
  <p><a href="empresa.php">Ir a Empresa</a></p>
  <p><a href="productos.php">Ir a Productos</a></p>
  <p><a href="galeria.php">Ir a Galería</a></p>
  <p><a href="contacto.php">Ir a Contacto</a></p>
  <div class=" text-center container-fluid "style="background-color: #fEfAEE;">
  <h2>Bienvenido</h2>
  <p>Esta es una tienda online de monkeys de BloonsTd6.</p>
</div>

  <div class="container-fluid my-4">
    <h5 class="fw-bold mb-3">Monkeys disponibles</h5>

    <!-- Este contenedor se llena dinámicamente desde creacion.js -->
    <div id="listaMonkeys" class="row g-3"></div>
  </div>

</div>


<footer class=" text-white text-center p-2 mt-10" style="background-color: #FF9800;">
  MiMonkey@bloons.com
</footer>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="creacion.js"></script>
<script src="manipulacion.js"></script>

</body>
</html>