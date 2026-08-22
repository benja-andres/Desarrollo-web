<?php
$mensaje = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mensaje = "Acceso correcto";
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
  
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <title>Acceso</title>
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
  <h2>Autenticar</h2>

  <?php if ($mensaje != "") { ?>
    <div class="alert alert-success">
      <?php echo $mensaje; ?>
    </div>
  <?php } ?>

  <form method="post">
    <div class="mb-3">
      <label class="form-label">Email:</label>
      <input type="text" name="correo" class="form-control" placeholder="Enter email">
    </div>

    <div class="mb-3">
      <label class="form-label">Password:</label>
      <input type="password" name="clave" class="form-control" placeholder="Enter password">
    </div>

    <div class="form-check mb-3">
      <input class="form-check-input" type="checkbox" id="recordar">
      <label class="form-check-label" for="recordar">Remember me</label>
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>
    <a href="index.php" class="btn btn-danger">Close</a>
  </form>
</div>

<footer class=" text-white text-center p-2 mt-5" style="background-color: #FF9800;">
  MiMonkey@bloons.com
</footer>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
