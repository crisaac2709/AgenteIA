# app/kb_cache.py
import time
from typing import Dict, Tuple

# importa tus funciones reales
from .utils import obtenerLlmEmbedding, obtenerLlm
from .utils import obtenerBaseDeConocimiento, crearSesionDeChat

# Creamos el primer LLM
LLM = obtenerLlm()

# 1) Crea el embedding UNA sola vez (gran boost si antes lo creabas en cada request)
LLM_EMBEDDING = obtenerLlmEmbedding()

# 2) Caché en memoria del proceso (clave: (user, coleccion))
_RETRIEVER_CACHE: Dict[Tuple[str, str], dict] = {}

# Ajustes del caché
CACHE_TTL_SECONDS = 60 * 30   # 30 min
CACHE_MAX_ITEMS   = 64        # capacidad máx.

def _evict_if_needed():
    # Si te pasas del límite, saca el más viejo
    if len(_RETRIEVER_CACHE) <= CACHE_MAX_ITEMS:
        return
    oldest_key = min(_RETRIEVER_CACHE, key=lambda k: _RETRIEVER_CACHE[k]["t"])
    _RETRIEVER_CACHE.pop(oldest_key, None)

def get_retriever(username: str, coleccion: str):
    """
    Devuelve un retriever desde caché si está fresco,
    si no, lo reconstruye y lo guarda.
    """
    key = (username, coleccion)
    now = time.time()
    entry = _RETRIEVER_CACHE.get(key)

    if entry and (now - entry["t"] < CACHE_TTL_SECONDS):
        return entry["ret"]

    # (re)construir desde tu storage persistente (Chroma en disco)
    ruta_BC = f"BaseConocimiento/{username}"
    retriever = obtenerBaseDeConocimiento(
        rutaDeBaseDeConocimiento=ruta_BC,
        coleccion=coleccion,
        llmEmbedding=LLM_EMBEDDING
    )

    _RETRIEVER_CACHE[key] = {"ret": retriever, "t": now}
    _evict_if_needed()
    return retriever




def drop_retriever(username: str, coleccion: str):
    """Si quieres invalidar manualmente una colección concreta."""
    _RETRIEVER_CACHE.pop((username, coleccion), None)
    
    
import time
_CHAT_CACHE = {}  
CHAT_TTL = 60 * 30

def get_chat_chain(username, coleccion, llm, personalidad, retriever):
    key = f"{username}:{coleccion}"
    now = time.time()
    hit = _CHAT_CACHE.get(key)
    if hit and hit["persona"] == (personalidad or "") and (now - hit["t"] < CHAT_TTL):
        hit["t"] = now
        return hit["chain"]
    from .utils import crearSesionDeChat
    chain = crearSesionDeChat(llm, personalidad, retriever)
    _CHAT_CACHE[key] = {"t": now, "chain": chain, "persona": (personalidad or "")}
    return chain
def drop_chat_chain(username: str, coleccion: str):
    _CHAT_CACHE.pop(f"{username}:{coleccion}", None)
