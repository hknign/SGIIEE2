function dibujarMapa() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    asientos.forEach(a => {
        let baseColor = "#777";

        if (a.zona === "vip") baseColor = "#ffd700";
        if (a.zona === "avanzado") baseColor = "#27ae60";
        if (a.zona === "normal") baseColor = "#7f8c8d";

        if (a.estado === "vendido") baseColor = "#e74c3c";
        if (a.estado === "apartado") baseColor = "#f1c40f";

        const px = (a.x / 100) * canvas.width;
        const py = (a.y / 100) * canvas.height;

        const radio = 14;

        ctx.beginPath();
        ctx.arc(px, py, radio, 0, Math.PI * 2);

        if (seleccionados.has(a.id)) ctx.fillStyle = "#3498db";
        else ctx.fillStyle = baseColor;

        ctx.fill();
        ctx.white = 2;
        ctx.strokeStyle = "#2c3e50";
        ctx.stroke();

        ctx.fillStyle = (a.zona === "vip") ? "black" : "white";
        ctx.font = "bold 11px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(a.codigo, px, py);
    });
}