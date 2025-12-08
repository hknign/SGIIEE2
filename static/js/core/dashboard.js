// ===============================
//   OBTENER CANVAS
// ===============================
const ctx1 = document.getElementById("graficoAsistencia");
const ctx2 = document.getElementById("graficoGanancias");

// Variables globales para evitar el error "canvas already in use"
let graficoAsistencia = null;
let graficoGanancias = null;

// ===============================
//   FUNCIÓN PARA CREAR GRÁFICOS
// ===============================
function crearGraficos() {

    // ---- Asegurar destrucción previa ----
    if (graficoAsistencia) graficoAsistencia.destroy();
    if (graficoGanancias) graficoGanancias.destroy();

    // ===============================
    //   GRÁFICO DE ASISTENCIA
    // ===============================
    graficoAsistencia = new Chart(ctx1, {
    type: "pie",
    data: {
        labels: ["Asistencia", "Inasistencia", "Reembolsos"],
        datasets: [{
            data: [62, 25, 13],
            backgroundColor: ["#27ae60", "#f1c40f", "#e74c3c"]
        }]
    },
    plugins: [ChartDataLabels],
    options: {
        plugins: {
            legend: {
                title: {
                        display: true,
                        text: "Asistencia al Evento",
                        font: {
                          size: 20,
                          weight: "bold"
                        },
                        color: "#000"
                    },
                labels: {
                    font: {
                        size: 16,   // ← aquí aumentas el tamaño de los labels
                        weight: "bold"
                    },
                    color: "#000" // opcional: color del texto
                }
            },
            datalabels: {
                color: "#fff",
                font: {
                    weight: "bold",
                    size: 14
                },
                formatter: (value, ctx) => {
                    const total = ctx.chart.data.datasets[0].data
                        .reduce((a, b) => a + b, 0);
                    return ((value / total) * 100).toFixed(1) + "%";
                }
            }
        }
    }
});

    // ===============================
    //   GRÁFICO DE GANANCIAS
    // ===============================
    graficoGanancias = new Chart(ctx2, {
        type: "doughnut",
        data: {
            labels: ["Ganancias", "Pérdidas", "Devoluciones"],
            datasets: [{
                data: [62, 25, 13],
                backgroundColor: ["#27ae60", "#f1c40f", "#e74c3c"]
            }]
        },
        plugins: [ChartDataLabels],
        options: {
            plugins: {
                legend: {
                    title: {
                        display: true,
                        text: "Ganancias y Pérdidas",
                        font: {
                          size: 20,
                          weight: "bold"
                        },
                        color: "#000"
                    },
                labels: {
                    font: {
                        size: 16,   // ← aquí aumentas el tamaño de los labels
                        weight: "bold"
                    },
                    color: "#000" // opcional: color del texto
                }
            },
                datalabels: {
                    color: "#fff",
                    font: {
                        weight: "bold",
                        size: 14
                    },
                    formatter: (value, ctx) => {
                        const total = ctx.chart.data.datasets[0].data
                            .reduce((a, b) => a + b, 0);
                        return ((value / total) * 100).toFixed(1) + "%";
                    }
                }
            }
        }
    });
}
new Chart(document.getElementById("chartLineaGanancias"), {
    type: "line",
    data: {
        labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
        datasets: [{
            label: "Ganancias mensuales",
            data: [100, 180, 90, 230, 190, 260],
            borderColor: "#3498db",
            backgroundColor: "rgba(52,152,219,0.2)",
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        plugins: {
            legend: { display: true }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
// ======================
// Sistema de filtros
// ======================

function obtenerDatosPorFiltro(filtro) {
    switch (filtro) {
        case "ultimo_evento":
            return { asistencia: [70, 20, 10], ganancias: [60, 30, 10] };
        case "ultimos_3":
            return { asistencia: [65, 25, 10], ganancias: [58, 32, 10] };
        case "ultima_semana":
            return { asistencia: [68, 22, 10], ganancias: [62, 28, 10] };
        case "mes":
            return { asistencia: [64, 26, 10], ganancias: [59, 31, 10] };
        case "anio":
            return { asistencia: [60, 30, 10], ganancias: [55, 35, 10] };
        default:
            return { asistencia: [62, 25, 13], ganancias: [62, 25, 13] };
    }
}

function actualizarGraficos(filtro) {
    const datos = obtenerDatosPorFiltro(filtro);

    graficoAsistencia.data.datasets[0].data = datos.asistencia;
    graficoGanancias.data.datasets[0].data = datos.ganancias;

    graficoAsistencia.update();
    graficoGanancias.update();
}

// ======================
// Botones del filtro
// ======================

document.querySelectorAll(".filtro-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        actualizarGraficos(btn.dataset.filtro);
    });
});



// Crear gráficos al cargar la página
crearGraficos();
