const API_URL = "http://127.0.0.1:8001/productos";
const API = "http://127.0.0.1:8001/";


// Selección de Elementos del DOM
const formProducto = document.getElementById("formProducto");
const tablaProductos = document.getElementById("tablaProductos");
const totalProductos = document.getElementById("totalProductos");


// 1. Función para Cargar Productos (GET)
async function cargarProductos() {
    try {
        const respuesta = await fetch(API_URL);
        const productos = await respuesta.json();

        tablaProductos.innerHTML = "";
        totalProductos.textContent = `${productos.length} productos`;

        if (productos.length === 0) {
            tablaProductos.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted py-4">
                        No hay productos registrados en la tiendita.
                    </td>
                </tr>`;
            return;
        }

        

        productos.forEach(p => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td class="fw-bold text-secondary">#${p.id}</td>
                <td>${p.nombre}</td>
                <td class="text-success fw-bold">$${p.precio}</td>
                <td>
                    <span class="badge ${p.cantidad < 10 ? 'bg-danger' : 'bg-success'}">
                        ${p.cantidad} unidades
                    </span>
                </td>
                <td class="text-end">
                    <button class="btn btn-outline-primary btn-sm" onclick="comprarProducto(${p.id})">
                        <i class="bi bi-trash"></i> Comprar
                    </button>
                </td>
                <td class="text-end">
                    <button class="btn btn-outline-danger btn-sm" onclick="eliminarProducto(${p.id})">
                        <i class="bi bi-trash"></i> Eliminar
                    </button>
                </td>
            `;
            tablaProductos.appendChild(fila);
        });

    } catch (error) {
        console.error("Error al cargar productos:", error);
    }
}

async function agregarProducto(event){
    event.preventDefault();

    var nombre = document.getElementById("nombre").value
    var precio = document.getElementById("precio").value
    var cantidad = document.getElementById("cantidad").value

    const nuevoContenido = {nombre, precio, cantidad}
    try {
        const respuesta = await fetch(API_URL, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(nuevoContenido)});

        if(respuesta.ok){
            formProducto.reset();
            await cargarProductos();
        }else{
            console.error("Hubo algo malo al guardar")
        }
    } catch (error) {
        console.log(error)
    }
}

async function eliminarProducto(id_producto){
    event.preventDefault();

    try {
        const respuesta = await fetch("http://127.0.0.1:8001/productos/"+id_producto, {method: "DELETE", headers: {"Content-Type": "application/json"}});

        if(respuesta.ok){
            await cargarProductos();
        }else{
            console.error("Hubo algo malo al eliminar")
        }
    } catch (error) {
        console.log(error)
    }
}

async function comprarProducto(id_producto){
    event.preventDefault();

    try {
        const respuesta = await fetch("http://127.0.0.1:8001/productos/"+id_producto, {method: "POST", headers: {"Content-Type": "application/json"}});

        if(respuesta.ok){
            await cargarProductos();
        }else{
            console.error("Hubo algo malo al eliminar")
        }
    } catch (error) {
        console.log(error)
    }
}


async function cargarAnalisis() {

    const respuesta = await fetch(
        "http://127.0.0.1:8001/analisis/ventas-producto"
    );

    const datos = await respuesta.json();

    const productos = datos.map(x => x.producto);

    const ventas = datos.map(x => x.ventas_totales);

    new Chart(
        document.getElementById("graficaVentas"),
        {
            type: "bar",

            data: {
                labels: productos,

                datasets: [{
                    label: "Ventas por producto",
                    data: ventas,
                    backgroundColor: "#0d6efd"
                }]
            },

            options: {
                responsive: true
            }
        }
    );
}


// Cargar catálogo al abrir la página
document.addEventListener("DOMContentLoaded", cargarProductos);


// Agregamos el evento para que se abre la función al dar clic en guardar producto
formProducto.addEventListener("submit", agregarProducto);

// ===============================
// DASHBOARD - INDICADORES
// ===============================

function formatoMoneda(valor) {
    return new Intl.NumberFormat("es-MX", {
        style: "currency",
        currency: "MXN"
    }).format(valor);
}

async function cargarResumen() {
    try {
        const respuesta = await fetch("http://127.0.0.1:8001/analisis/resumen");

        if (!respuesta.ok) {
            throw new Error("Error al consultar el resumen");
        }

        const datos = await respuesta.json();

        document.getElementById("totalVentas").textContent =
            formatoMoneda(datos.ventas_totales);

        document.getElementById("unidadesVendidas").textContent =
            datos.unidades_vendidas;

        document.getElementById("valorInventario").textContent =
            formatoMoneda(datos.valor_inventario);

    } catch (error) {
        console.error("Error al cargar indicadores:", error);
    }
}

// Cargar indicadores al abrir la página
document.addEventListener("DOMContentLoaded", () => {
    cargarResumen();
    cargarGraficaVentas();
    cargarGraficaProductos();
    cargarGraficaDiaria();
});

// ===============================
// GRÁFICA DE VENTAS POR PRODUCTO
// ===============================

let graficaVentas = null;

async function cargarGraficaVentas() {
    try {
        const respuesta = await fetch(
            "http://127.0.0.1:8001/analisis/ventas-producto"
        );

        if (!respuesta.ok) {
            throw new Error("Error al consultar ventas por producto");
        }

        const datos = await respuesta.json();

        const etiquetas = datos.map(item => item.producto);
        const valores = datos.map(item => item.ventas_totales);

        const contexto = document.getElementById("graficaVentas");

        // Evitar duplicar la gráfica al actualizar
        if (graficaVentas) {
            graficaVentas.destroy();
        }

        graficaVentas = new Chart(contexto, {
            type: "bar",

            data: {
                labels: etiquetas,

                datasets: [{
                    label: "Ventas totales",
                    data: valores,
                    backgroundColor: "#0d6efd",
                    borderRadius: 5
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        display: false
                    },

                    tooltip: {
                        callbacks: {
                            label: function(contexto) {
                                return formatoMoneda(contexto.raw);
                            }
                        }
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(valor) {
                                return formatoMoneda(valor);
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error al cargar gráfica de ventas:", error);
    }
}

// ===============================
// GRÁFICA DE PARTICIPACIÓN
// ===============================

let graficaProductos = null;

async function cargarGraficaProductos() {
    try {
        const respuesta = await fetch(
            "http://127.0.0.1:8001/analisis/ventas-producto"
        );

        if (!respuesta.ok) {
            throw new Error("Error al consultar productos");
        }

        const datos = await respuesta.json();

        const etiquetas = datos.map(item => item.producto);
        const valores = datos.map(item => item.ventas_totales);

        const contexto = document.getElementById("graficaProductos");

        if (graficaProductos) {
            graficaProductos.destroy();
        }

        graficaProductos = new Chart(contexto, {
            type: "doughnut",

            data: {
                labels: etiquetas,

                datasets: [{
                    data: valores,
                    borderWidth: 2
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        position: "bottom"
                    },

                    tooltip: {
                        callbacks: {
                            label: function(contexto) {
                                const total = contexto.dataset.data.reduce(
                                    (a, b) => a + b, 0
                                );

                                const porcentaje =
                                    (contexto.raw / total) * 100;

                                return `${contexto.label}: ${
                                    formatoMoneda(contexto.raw)
                                } (${porcentaje.toFixed(1)}%)`;
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error al cargar participación:", error);
    }
}

// ===============================
// GRÁFICA DE EVOLUCIÓN DIARIA
// ===============================

let graficaDiaria = null;

async function cargarGraficaDiaria() {
    try {
        const respuesta = await fetch(
            "http://127.0.0.1:8001/analisis/ventas-dia"
        );

        if (!respuesta.ok) {
            throw new Error("Error al consultar ventas diarias");
        }

        const datos = await respuesta.json();

        const etiquetas = datos.map(item => item.dia);
        const valores = datos.map(item => item.ventas_totales);

        const contexto = document.getElementById("graficaDiaria");

        if (graficaDiaria) {
            graficaDiaria.destroy();
        }

        graficaDiaria = new Chart(contexto, {
            type: "line",

            data: {
                labels: etiquetas,

                datasets: [{
                    label: "Ventas diarias",
                    data: valores,
                    borderColor: "#0d6efd",
                    backgroundColor: "rgba(13, 110, 253, 0.15)",
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(contexto) {
                                return formatoMoneda(contexto.raw);
                            }
                        }
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(valor) {
                                return formatoMoneda(valor);
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error al cargar evolución diaria:", error);
    }
}