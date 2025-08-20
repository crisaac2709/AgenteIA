(function crearBaseConocimiento() {
    const formColeccion = document.getElementById('form-coleccion')
    const url = window.URLS?.url_coleccion
    const mensaje = document.getElementById('messages_coleccion')

    console.log(url);

    if (!url || !formColeccion) {
        console.error("Falta url o form");
    }

    formColeccion.addEventListener('submit', async (e) => {
        e.preventDefault()

        const formData = new FormData(formColeccion)
        const csrfFromInput = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const csrf = csrfFromInput || getCookie('csrftoken');

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrf,             
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: "same-origin"
            })

            const data = await response.json()

            if (data.ok) {
                mensaje.textContent = data.respuesta
                localStorage.setItem('coleccion_actual', formData.get('coleccion'))
            } else {
                console.log(data.errors)
            }

        } catch(err) {
            console.error(err.message)
        }
    })


    function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
})()