// 1. Simulación de datos de una API
// respuestaAPI = apicall(); // GET https://monkeystore.cl/api/monkeys
const respuestaAPI = {
    status: 200,
    mensaje: "Monkeys obtenidos correctamente",
    data: [
        { id: 1, nombre: "Dart Monkey", tipo: "Básico", precio: 200 },
        { id: 2, nombre: "Ninja Monkey", tipo: "Militar", precio: 500 },
        { id: 3, nombre: "Sniper Monkey", tipo: "Militar", precio: 350 },
        { id: 4, nombre: "Super Monkey", tipo: "Poder Mágico", precio: 2500 }
    ]
};

// 2. Función para crear elementos dinámicamente en runtime
function generarMonkeysDinamicos() {
    // Buscamos el contenedor donde se van a mostrar las tarjetas
    const contenedorMonkeys = document.querySelector('#listaMonkeys');

    if (!contenedorMonkeys) return;

    // Recorremos los datos simulados
    respuestaAPI.data.forEach(monkey => {
        // A. Crear el elemento contenedor de columna con document.createElement
        const columna = document.createElement('div');
        columna.className = 'col-sm-6 col-lg-3';

        // B. Crear la tarjeta y asignarle clases de Bootstrap por código
        const tarjeta = document.createElement('div');
        tarjeta.className = 'card shadow-sm border-0 tarjeta-monkey';
        tarjeta.setAttribute('data-id', monkey.id);

        // C. Rellenar la estructura interna con innerHTML
        tarjeta.innerHTML = `
            <div class="card-body text-center">
                <span class="badge bg-secondary mb-2">${monkey.tipo}</span>
                <h6 class="card-title fw-bold">${monkey.nombre}</h6>
                <p class="card-text text-muted mb-2">$${monkey.precio}</p>
                <button class="btn btn-outline-success btn-sm btn-comprar">Comprar (<span>0</span>)</button>
            </div>
        `;

        // D. Agregar la tarjeta dentro de la columna, y la columna dentro del contenedor
        columna.appendChild(tarjeta);
        contenedorMonkeys.appendChild(columna);
    });
}

// Ejecutar la función al cargar la página
window.addEventListener('DOMContentLoaded', generarMonkeysDinamicos);