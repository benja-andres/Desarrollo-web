<!DOCTYPE html>
<html lang="es">
<head>
  
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <title>Galería</title>
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


<div class="container mt-4">
  <h2>Galería</h2>
  <p>Galeria de los monkeys.</p>

  <div id="carruselFotos" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">

      <div class="carousel-item active">
        <img src="imagen1.png" class="d-block w-100" alt="Imagen 1">
      </div>

      <div class="carousel-item">
        <img src="thumb-1920-1206422.jpg" class="d-block w-100" alt="Imagen 2">
      </div>

      <div class="carousel-item">
        <img src="1330944-Bloons-TD-6-HD-Wallpaper.jpg" class="d-block w-100" alt="Imagen 3">
      </div>

      <div class="carousel-item">
        <img src="wp7501271.jpg" class="d-block w-100" alt="Imagen 4">
      </div>

    </div>

    <button class="carousel-control-prev" type="button" data-bs-target="#carruselFotos" data-bs-slide="prev">
      <span class="carousel-control-prev-icon"></span>
    </button>

    <button class="carousel-control-next" type="button" data-bs-target="#carruselFotos" data-bs-slide="next">
      <span class="carousel-control-next-icon"></span>
    </button>
  </div>
</div>

<footer class=" text-white text-center p-2 mt-5" style="background-color: #FF9800;">
  MiMonkey@bloons.com
</footer>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
