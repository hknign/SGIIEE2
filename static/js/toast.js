function mostrarToast(texto) {
    const id = "toast-contenedor";
    let cont = document.getElementById(id);

    if (!cont) {
        cont = document.createElement("div");
        cont.id = id;
        cont.style.position = "fixed";
        cont.style.top = "30px";
        cont.style.right = "30px";
        cont.style.zIndex = 5000;
        document.body.appendChild(cont);
    }

    const t = document.createElement("div");
    t.className = "toast align-items-center text-bg-dark border-0 show mb-2";
    t.role = "alert";

    t.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${texto}</div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    cont.appendChild(t);

    setTimeout(() => t.remove(), 3000);
}
