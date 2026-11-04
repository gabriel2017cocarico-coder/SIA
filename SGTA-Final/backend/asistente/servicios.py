"""
asistente/servicios.py

Cliente HTTP para comunicarse con el motor de IA local (Ollama).
La URL del servicio se lee desde la variable de entorno OLLAMA_HOST.
Si Ollama no está disponible, retorna un mensaje de contingencia
sin lanzar excepciones hacia el llamador.
"""

import os
import requests


# ==============================================================
# CONFIGURACIÓN
# ==============================================================

OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_HOST",
    "http://localhost:11434"
).rstrip("/")

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "sigta-ai")

OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "30"))

MENSAJE_NO_DISPONIBLE = (
    "El asistente de inteligencia artificial no está disponible "
    "en este momento. Por favor, intente nuevamente en unos instantes."
)


# ==============================================================
# CLIENTE OLLAMA
# ==============================================================

def consultar_ollama(prompt: str) -> str:
    """
    Envía el prompt al modelo Ollama y retorna la respuesta
    como texto plano.

    Parámetros:
        prompt (str): Texto completo a enviar al modelo, incluyendo
                      el contexto del sistema ya inyectado.

    Retorna:
        str: Texto de respuesta generado por el modelo, o el mensaje
             de contingencia si el servicio no está disponible.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        respuesta = requests.post(
            url,
            json=payload,
            timeout=OLLAMA_TIMEOUT,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        # Ollama no está corriendo o el puerto no es accesible
        return MENSAJE_NO_DISPONIBLE

    except requests.exceptions.Timeout:
        # El modelo tardó demasiado
        return MENSAJE_NO_DISPONIBLE

    except requests.exceptions.HTTPError:
        # Respuesta HTTP con código de error (4xx, 5xx)
        return MENSAJE_NO_DISPONIBLE

    except Exception:
        # Cualquier otro fallo inesperado
        return MENSAJE_NO_DISPONIBLE
