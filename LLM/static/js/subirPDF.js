// static/js/subirPDF.js
(function () {
  const form = document.getElementById('form-pdf');
  const messages = document.getElementById('messages');
  const resultado = document.getElementById('resultado');

  year.textContent = anioActual

  // URL entregada por el template
  const url = window.URLS?.subir_pdf_ajax;

  if (!form || !url) {
    console.error('Falta el form o window.URLS.subir_pdf_ajax.');
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    messages.textContent = 'Subiendo...';
    resultado.innerHTML = '';

    const fd = new FormData(form);

    // Toma el token del input hidden o de la cookie (por si CSRF_COOKIE_HTTPONLY está True)
    const csrfFromInput = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const csrf = csrfFromInput || getCookie('csrftoken');

    try {
      const resp = await fetch(url, {
        method: 'POST',
        body: fd,
        headers: {
          'X-CSRFToken': csrf,                  // 👈 nombre correcto
          'X-Requested-With': 'XMLHttpRequest', // opcional, pero útil
        },
        credentials: 'same-origin', // asegura envío de cookies
      });

      const ct = resp.headers.get('content-type') || '';
      let payload, text;

      if (ct.includes('application/json')) {
        payload = await resp.json();
      } else {
        text = await resp.text();
      }

      if (!resp.ok) {
        // Errores de validación o 4xx/5xx
        messages.textContent = 'Errores de validación';
        const errs = (payload && payload.errors) || { server: [text || `HTTP ${resp.status}`] };
        resultado.innerHTML = Object.entries(errs)
          .map(([campo, lista]) => `<p><b>${campo}:</b> ${lista.join(', ')}</p>`)
          .join('');
        return;
      }

      if (!payload) {
        throw new Error(`Respuesta no JSON: ${String(text).slice(0, 200)}...`);
      }

      // Éxito
      if (!payload.ok) {
        // Por si el backend devuelve 200 pero ok=False
        messages.textContent = 'Errores de validación';
        const errs = payload.errors || { server: ['Respuesta con ok=False'] };
        resultado.innerHTML = Object.entries(errs)
          .map(([campo, lista]) => `<p><b>${campo}:</b> ${lista.join(', ')}</p>`)
          .join('');
        return;
      }

      messages.textContent = '¡Subido!';
      resultado.innerHTML = `
        <p><b>${payload.titulo}</b> subido correctamente.</p>
        <p><a href="${payload.url}" target="_blank" rel="noopener">Abrir archivo</a></p>
        <embed src="${payload.url}" type="application/pdf" width="100%" height="400">
      `;
      form.reset();

    } catch (err) {
      console.error(err);
      messages.textContent = 'Error de red o servidor';
    }
  });

  // Helpers
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
})();
