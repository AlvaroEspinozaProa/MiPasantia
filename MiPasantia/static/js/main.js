// Muestra el nombre del archivo elegido antes de enviar una publicación.
document.querySelectorAll('input[type="file"]').forEach((input) => {
    input.addEventListener("change", () => {
        const ayuda = input.closest("label")?.querySelector("small");
        if (ayuda && input.files[0]) {
            ayuda.textContent = "Archivo seleccionado: " + input.files[0].name;
        }
    });
});
