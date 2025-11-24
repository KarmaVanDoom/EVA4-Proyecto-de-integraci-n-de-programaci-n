function formatRut(value) {
    value = value.replace(/[^0-9kK]/g, "").toUpperCase();
    if (value.length <= 1) return value;

    let cuerpo = value.slice(0, -1);
    let dv = value.slice(-1);

    cuerpo = cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    return cuerpo + "-" + dv;
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_rut");

    if (!input) return;

    input.addEventListener("input", function () {
        const start = input.selectionStart;
        input.value = formatRut(input.value);
        input.setSelectionRange(start, start);
    });
});
