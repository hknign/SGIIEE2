canvas.addEventListener("click", function (e) {
    const rect = canvas.getBoundingClientRect();

    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const cx = (e.clientX - rect.left) * scaleX;
    const cy = (e.clientY - rect.top) * scaleY;

    for (let a of asientos) {
        const px = (a.x / 100) * canvas.width;
        const py = (a.y / 100) * canvas.height;
        const dist = Math.hypot(cx - px, cy - py);

        if (dist <= 14 && a.estado === "disponible") {
            if (seleccionados.has(a.id)) seleccionados.delete(a.id);
            else seleccionados.add(a.id);

            actualizarContador();
            resaltarFilaTabla(a.id);
            dibujarMapa();
            break;
        }
    }
});

function actualizarContador() {
    document.getElementById("contadorSeleccionados").textContent =
        seleccionados.size;
}

function resaltarFilaTabla(idAsiento) {
    const filas = document.querySelectorAll("#tablaAsientos tr[data-id]");
    filas.forEach(f => {
        const id = parseInt(f.dataset.id, 10);
        if (seleccionados.has(id)) f.classList.add("table-primary");
        else f.classList.remove("table-primary");
    });
}
