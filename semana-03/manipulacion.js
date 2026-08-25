// 1. Gestión avanzada de objetos en runtime

const inventarioMonkeys = {
    dart: { id: 1, estado: "Disponible", enOferta: true },
    ninja: { id: 2, estado: "Disponible", enOferta: false },
    borrador: { id: 99, estado: "Descontinuado", enOferta: false }
};

// Recorrer entradas con Object.entries()
console.log("--- Inventario inicial ---");
for (const [clave, valor] of Object.entries(inventarioMonkeys)) {
    console.log(`Monkey: ${clave} / ID: ${valor.id} / Estado: ${valor.estado}`);
}

// Borrar una propiedad del objeto con 'delete'
delete inventarioMonkeys.borrador;
console.log("--- Inventario después de usar 'delete' ---", inventarioMonkeys);

// 2. Modificación y eventos del DOM

window.addEventListener('DOMContentLoaded', () => {
    // Esperamos a que creacion.js ya haya insertado las tarjetas en el DOM
    setTimeout(() => {
        const contenedorMonkeys = document.querySelector('#listaMonkeys');
        if (!contenedorMonkeys) return;

        // Delegación de eventos: un solo listener para todos los botones "Comprar"
        contenedorMonkeys.addEventListener('click', (evento) => {

            if (evento.target.closest('.btn-comprar')) {
                const boton = evento.target.closest('.btn-comprar');
                const spanContador = boton.querySelector('span');

                let comprasActuales = parseInt(spanContador.textContent);
                spanContador.textContent = comprasActuales + 1;

                // Actualización de estado visual (DOM) con classList
                boton.classList.remove('btn-outline-success');
                boton.classList.add('btn-success');

                console.log("Se actualizó el estado: compra registrada en el DOM");

                // Eliminar el elemento del DOM al agotar el stock
                if (comprasActuales > 4) {
                    const tarjeta = boton.closest('.tarjeta-monkey');
                    const columna = tarjeta ? tarjeta.closest('.col-sm-6, .col-lg-3') : null;

                    if (columna) {
                        columna.remove();
                        console.log("Monkey agotado: elemento eliminado del DOM");
                    }
                }
            }
        });

    }, 300);
});