function formatRut(value) {
    value = value.replace(/[^0-9kK]/g, "").toUpperCase();
    if (value.length <= 1) return value;

    let cuerpo = value.slice(0, -1);
    let dv = value.slice(-1);

    cuerpo = cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    return cuerpo + "-" + dv;
}

document.addEventListener("DOMContentLoaded", function () {
    // Array para almacenar los inputs a formatear
    const inputsToFormat = [];

    // Buscar inputs de RUT (id="id_rut")
    const rutInputs = document.querySelectorAll('input[id="id_rut"]');
    rutInputs.forEach(input => inputsToFormat.push(input));

    // Para el login, agregar el campo username si existe el campo de password
    const usernameInput = document.querySelector('input[id="id_username"]');
    const passwordInput = document.querySelector('input[id="login_pass"]');

    if (usernameInput && passwordInput) {
        // Estamos en la página de login
        inputsToFormat.push(usernameInput);
    }

    // Aplicar el formateador a todos los inputs seleccionados
    inputsToFormat.forEach(function (input) {
        if (!input) return;

        input.addEventListener("input", function () {
            const start = input.selectionStart;
            const prevLength = input.value.length;
            input.value = formatRut(input.value);
            const newLength = input.value.length;

            // Ajustar la posición del cursor considerando los caracteres agregados
            const diff = newLength - prevLength;
            input.setSelectionRange(start + diff, start + diff);
        });
    });
});
