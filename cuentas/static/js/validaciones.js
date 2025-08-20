const mensaje = document.querySelectorAll('.mensaje')
const username = document.getElementById('username')
const first_name = document.getElementById('first_name')
const last_name = document.getElementById('last_name')
const email = document.getElementById('email')
const password = document.getElementById('password')
const telefono = document.getElementById('telefono')
const fecha_nacimiento = document.getElementById('fecha_nacimiento')


let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
let passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$/;
let patron = /^\d{10}$/;


function validar(campo, num_campo, longitud, mensaje_valido, mensaje_invalido) {
    campo.addEventListener('input', () => {
        const msg = mensaje[num_campo]
        if (campo.value.length >= longitud) {
            msg.textContent = mensaje_valido
            msg.className = 'mensaje valido'
        } else {
            msg.textContent = mensaje_invalido
            msg.className = 'mensaje invalido'
        }
    })
}

function otra_validacion(campo, num_campo, regex, mensaje_valido, mensaje_invalido) {
    campo.addEventListener('input', () => {
        const msg = mensaje[num_campo]
        if (regex.test(campo.value)) {
            msg.textContent = mensaje_valido
            msg.className = 'mensaje valido'
        } else {
            msg.textContent = mensaje_invalido
            msg.className = 'mensaje invalido'
        }
    })
}

validar(username, 0, 8, 'Usuario valido', 'Usuario Invalido. Minimo 8 caracteres')
validar(first_name, 1, 3, 'Nombre valido', 'Nombre Invalido. Minimo 3 caracteres')
validar(last_name, 2, 3, 'Apellido valido', 'Apellido Invalido. Minimo 3 caracteres')
otra_validacion(email, 3, emailRegex, 'Correo valido', 'Correo invalido')
otra_validacion(password, 4, passRegex, 'Contraseña valida', 'Min 8 caracteres, Max 20 caracteres, una mayuscula, minusculas y un numero.')
otra_validacion(telefono, 5, patron, 'Telefono valido', 'Se necesita exactamente 10 caracteres')

fecha_nacimiento.addEventListener('input', () => {
    const hoy = new Date()
    const msg = mensaje[6]
    const fechaNacimientoDate = new Date(fecha_nacimiento.value)
    if (fechaNacimientoDate > hoy) {
        msg.textContent = 'La fecha de nacimiento no puede ser mayor a la fecha actual'
        msg.className = 'mensaje invalido'
    } else {
        msg.textContent = 'Fecha valida'
        msg.className = 'mensaje valido'
    }
})

const inputFoto = document.getElementById('foto');
const preview   = document.getElementById('preview');
inputFoto?.addEventListener('change', (e) => {
    const file = e.target.files?.[0];
    if (!file) { preview.innerHTML = ''; return; }
    const url = URL.createObjectURL(file);
    preview.innerHTML = `<img src="${url}" alt="Vista previa">`;
});


