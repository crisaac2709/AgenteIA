(function guardarContexto() {
    const formContexto = document.getElementById('form-contexto')
    const url = window.URLS?.url_contexto
    const mensaje = document.getElementById('messages_contexto')

    console.log(url);

    if (!url || !formContexto) {
        console.error("Falta url o form");
    }

    formContexto.addEventListener('submit', async (e) => {
        e.preventDefault()

        const formData = new FormData(formContexto)
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