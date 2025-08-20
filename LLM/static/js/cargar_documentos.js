(function cargarDocumentos() {
    const formCarga = document.getElementById('form-carga')
    const url = window.URLS?.url_cargar_documentos
    const mensaje = document.getElementById('messages_carga')
    const coleccion = localStorage.getItem('coleccion_actual')

    console.log(url);

    if (!url || !formCarga) {
        console.error("Falta url o form");
    }

    formCarga.addEventListener('submit', async (e) => {
        e.preventDefault()

        console.log('La coleccion es: ',coleccion);
        if (!coleccion) {
            mensaje.textContent = 'Falta coleccion'
            return
        }

        const formData = new FormData(formCarga)

        formData.append('coleccion', coleccion)
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

                setTimeout(() => {
                    mensaje.textContent = ''
                },2000)
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