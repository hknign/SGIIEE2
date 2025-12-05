function filtrarTabla() {
    const estado = document.getElementById("filtroEstado").value;
    const zona = document.getElementById("filtroZona").value;

    const filas = document.querySelectorAll("#tablaAsientos tr[data-id]");
    filas.forEach(fila => {
        const filaEstado = fila.dataset.estado;
        const filaZona = fila.dataset.zona;

        let mostrar = true;
        if (estado && filaEstado !== estado) mostrar = false;
        if (zona && filaZona !== zona) mostrar = false;

        fila.style.display = mostrar ? "" : "none";
    });
}

document.getElementById("filtroEstado").addEventListener("change", filtrarTabla);
document.getElementById("filtroZona").addEventListener("change", filtrarTabla);
document.getElementById("btnLimpiarFiltros").addEventListener("click", () => {
    document.getElementById("filtroEstado").value = "";
    document.getElementById("filtroZona").value = "";
    filtrarTabla();
});
