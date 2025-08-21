(function obtenerBaseConocimiento() {
    const formBC = document.getElementById('form-bc')
    const url = window.URLS?.url_base_conocimiento
    const mensaje = document.getElementById('messages_bc')
    const coleccion = localStorage.getItem('coleccion')

    console.log(url);

    if (!url || !formBC) {
        console.error("Falta url o form");
    }

    formBC.addEventListener('submit', async (e) => {
        e.preventDefault()

        const formData = new FormData(formBC)
        const csrfFromInput = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const csrf = csrfFromInput || getCookie('csrftoken');

        formData.append('coleccion',coleccion)

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
                mensaje.textContent = data.mensaje
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