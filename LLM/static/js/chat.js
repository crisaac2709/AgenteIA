
(function chatApi() {
  const formChat   = document.getElementById('form-chat');
  const textarea   = document.getElementById('prompt');
  const chatBox    = document.querySelector('.chat-messages');
  const url        = window.URLS?.url_chat;
  const contexto   = localStorage.getItem('contexto') || '';
  const coleccion = localStorage.getItem('coleccion_actual') || '';

  if (!formChat || !url || !chatBox) {
    console.error('Falta url_chat, form-chat o .chat-messages');
    return;
  }

  formChat.addEventListener('submit', async (e) => {
    e.preventDefault();
    const mensaje = (textarea.value || '').trim();
    if (!mensaje) return;

    // 1) pinta mensaje del usuario
    addMsg('user', mensaje, `Tú · ${timeNow()}`);
    textarea.value = '';

    // 2) muestra “typing…” del agente
    const typingEl = addTyping();

    // 3) arma el FormData para tu vista Django
    const fd = new FormData();
    fd.append('mensaje', mensaje);
    if (contexto)  fd.append('contexto', contexto);
    if (coleccion) fd.append('coleccion', coleccion)

    // CSRF
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: fd,
        headers: {
          'X-CSRFToken': csrf,
          'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin'
      });

      const data = await response.json();
      typingEl.remove();

      if (!response.ok || !data.ok) {
        addMsg('agent', data.error || data.errors || 'Hubo un problema procesando tu mensaje.', `Agente · ${timeNow()}`);
        return;
      }

      // 4) pinta respuesta del agente
      let answer = '';
      if (data.respuesta) {
        // si tu backend ya arma la respuesta final
        answer = data.respuesta;
      } else if (Array.isArray(data.resultados) && data.resultados.length) {
        // si devuelves snippets/previas de RAG
        answer = 'Encontré esto:\n' + data.resultados
          .map((r, i) => `• (${i + 1}) ${r.source}: ${r.preview}`)
          .join('\n');
      } else {
        answer = 'No encontré información relevante en la base.';
      }

      addMsg('agent', answer, `Agente · ${timeNow()}`);
    } catch (err) {
      typingEl.remove();
      addMsg('agent', 'Error de red. Inténtalo nuevamente.', `Agente · ${timeNow()}`);
      console.error(err);
    }
  });

  // Helpers UI
  function addMsg(from, text, meta) {
    const wrap   = document.createElement('div');
    wrap.className = `msg ${from === 'user' ? 'from-user' : 'from-agent'}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = from === 'user' ? '🧑' : '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    // soporta múltiples líneas
    (text || '').split('\n').forEach(line => {
      const p = document.createElement('p');
      p.textContent = line;
      bubble.appendChild(p);
    });

    const span = document.createElement('span');
    span.className = 'meta';
    span.textContent = meta;

    bubble.appendChild(span);
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    chatBox.appendChild(wrap);
    scrollBottom();
  }

  function addTyping() {
    const wrap   = document.createElement('div');
    wrap.className = 'msg from-agent';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    const p = document.createElement('p');
    p.textContent = 'Procesando…';

    const typing = document.createElement('div');
    typing.className = 'typing';
    typing.innerHTML = '<i></i><i></i><i></i>';

    const meta = document.createElement('span');
    meta.className = 'meta';
    meta.textContent = 'Agente · escribiendo…';

    bubble.appendChild(p);
    bubble.appendChild(typing);
    bubble.appendChild(meta);
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    chatBox.appendChild(wrap);
    scrollBottom();
    return wrap;
  }

  function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function timeNow() {
    try {
      return new Date().toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit' });
    } catch {
      return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  }

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
})();

