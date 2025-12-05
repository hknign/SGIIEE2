function csrftoken() {
    const v = document.cookie.match("(^|;)\\s*csrftoken\\s*=\\s*([^;]+)");
    return v ? v.pop() : "";
}

    document.getElementById("btnAgregarCarrito").addEventListener("click", function () {
    if (seleccionados.size === 0) {
        alert("No has seleccionado asientos.");
        return;
    }

    const url = this.dataset.url;  // ← aquí obtienes la URL real

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            asientos: Array.from(seleccionados)
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.ok) {
            alert("Asientos agregados correctamente.");
            window.location.reload();
        } else {
            alert(data.error);
        }
    })
    .catch(() => alert("Error al comunicarse con el servidor."));
});
