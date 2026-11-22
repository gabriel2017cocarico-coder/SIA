"""

asistente/views.py



Endpoint principal del asistente de IA del sistema SIGTA.



Ruta: POST /api/asistente/chat/

Autenticación: Token requerido (IsAuthenticated).

Body JSON: { "mensaje": "texto del usuario" }

Respuesta: { "respuesta": "texto del asistente" }



El endpoint es tolerante a fallos: si Ollama no está disponible,

devuelve un mensaje de contingencia con HTTP 200 para no

interrumpir la experiencia del usuario en el frontend.

"""



from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import status

import json

import logging

import re

from difflib import get_close_matches



from django.http import HttpResponse, StreamingHttpResponse



from . import voz

from .contexto import obtener_contexto

from .servicios import INSTRUCCION_IDENTIDAD, consultar_ollama, consultar_ollama_stream

from .consultas import ConsultasConversacionales

from usuarios.models import UsuarioRol





# ==============================================================

# VISTA PRINCIPAL

# ==============================================================



MAX_PANTALLA = 1500

logger = logging.getLogger(__name__)



INSTRUCCION_VOZ = (

    "=== FORMATO DE RESPUESTA (MODO VOZ) ===\n"

    "Tu respuesta se leerá en voz alta. Responde en máximo tres frases cortas y directas, "

    "sin emojis, sin listas, sin viñetas, sin asteriscos ni formato markdown. "

    "Di los números con claridad y no repitas la pregunta."

)



class ChatAsistenteView(APIView):

    """

    Recibe el mensaje del usuario, inyecta el contexto operativo

    real del sistema, consulta Ollama y retorna la respuesta.

    """



    permission_classes = [IsAuthenticated]



    def post(self, request):



        # ----------------------------------------------------------

        # 1. Validar entrada

        # ----------------------------------------------------------

        mensaje = request.data.get("mensaje", "").strip()



        if not mensaje:

            return Response(

                {"error": "El campo 'mensaje' es requerido y no puede estar vacío."},

                status=status.HTTP_400_BAD_REQUEST,

            )



        if len(mensaje) > 2000:

            return Response(

                {"error": "El mensaje no puede superar los 2000 caracteres."},

                status=status.HTTP_400_BAD_REQUEST,

            )



        historial_recibido = request.data.get("historial", [])

        historial = []

        if isinstance(historial_recibido, list):

            for item in historial_recibido[-8:]:

                if not isinstance(item, dict) or item.get("rol") not in ("usuario", "bot"):

                    continue

                texto_previo = str(item.get("texto", ""))[:500].strip()

                if texto_previo:

                    historial.append({"rol": item["rol"], "texto": texto_previo})



        texto = mensaje.casefold().translate(str.maketrans("áéíóú", "aeiou"))

        es_creacion = bool(re.search(

            r"\b(?:cre\w*|gener\w*|registr\w*|abr\w*|levant\w*|hac\w*)\b.{0,40}\b(?:ticket|solicitud|orden|requerimiento)\b",

            texto,

        )) or any(x in texto for x in (

            "reportar una falla", "solicitar mantenimiento", "crear solicitud",

            "creame una solicitud", "registra una solicitud",

        ))

        if es_creacion:

            mantenimiento = any(x in texto for x in (

                "mantenimiento", "aire", "puerta", "luz", "infraestructura",

                "electricidad", "cerradura", "pintura", "pared", "grifo",

                "fuga", "techo", "agua", "mueble", "ventana",

            ))

            soporte = any(x in texto for x in (

                "soporte", "utic", "computadora", "internet", "wifi",

                "red", "impresora", "laptop", "proyector", "software",

            ))

            categoria = "MANTENIMIENTO" if mantenimiento else ("SOPORTE" if soporte else "ELEGIR_TIPO")

            return Response({

                "respuesta": "Claro, lo armamos juntos. Te pediré los datos necesarios y te mostraré un resumen para confirmar antes de registrarlo.",

                "accion": {"tipo": "CREAR_SOLICITUD", "categoria": categoria},

            }, status=status.HTTP_200_OK)

        # ----------------------------------------------------------
        # Consultas operativas directas (conteo, urgencia, estados)
        # ----------------------------------------------------------
        try:
            consulta = ConsultasConversacionales(request.user).buscar(mensaje, historial)
        except Exception:
            logger.exception("No se pudo resolver la consulta conversacional del usuario %s", request.user.pk)
            consulta = None
        if consulta:
            payload = {"respuesta": consulta}
            # Si el usuario además pidió que lo lleven a la solicitud o al ticket, disparamos navegación a sus solicitudes
            if re.search(r"\b(?:llev\w*|ir|entra\w*|abre\w*|muestra\w*|ver)\b", texto):
                payload["accion"] = {"tipo": "NAVEGACION", "ruta": "/usuario/mis-solicitudes"}
            return Response(payload, status=status.HTTP_200_OK)

        intencion_navegar = bool(re.search(

            r"\b(?:llev\w*|navega\w*|ir|entra\w*|abre\w*|accede\w*|muestra\w*|dirige\w*|manda\w*|pasa\w*|ver|consulta\w*|revisa\w*|busca\w*|ensena\w*|mira\w*)\b",

            texto,

        )) or any(x in texto for x in (

            "quiero ir", "quiero entrar", "quiero ver", "puedes llevar",

            "donde veo", "donde encuentro", "como llego", "mi inicio", "mi panel",

        ))

        if intencion_navegar:

            roles = set(UsuarioRol.objects.filter(usuario=request.user, activo=True).values_list("rol__codigo", flat=True))

            rol_principal = next((r for r in (

                "ADMIN", "SUPERUSER", "JEFE_UTIC", "ESPECIALISTA", "SERVICIOS_GENERALES",

                "AUXILIAR_SERVICIOS_GENERALES", "DAF", "TESORERIA",

                "ENCARGADO_COMPRAS_ALMACEN", "SOLICITANTE",

            ) if r in roles), "SUPERUSER" if request.user.is_superuser else "SOLICITANTE")

            ruta_inicio = {

                "ADMIN": "/admin/dashboard", "SUPERUSER": "/superuser/dashboard",

                "JEFE_UTIC": "/jefe-utic/dashboard", "ESPECIALISTA": "/especialista/dashboard",

                "SERVICIOS_GENERALES": "/servicios-generales/dashboard",

                "AUXILIAR_SERVICIOS_GENERALES": "/auxiliar-servicios-generales/dashboard",

                "DAF": "/daf/dashboard", "TESORERIA": "/tesoreria/dashboard",

                "ENCARGADO_COMPRAS_ALMACEN": "/almacen/dashboard", "SOLICITANTE": "/usuario/dashboard",

            }[rol_principal]



            destino = None

            respuesta_navegacion = "Abriendo esa sección."

            if any(x in texto for x in ("dashboard", "mi inicio", "mi panel", "panel principal")):

                destino, respuesta_navegacion = ruta_inicio, "Abriendo tu panel principal."

            elif any(x in texto for x in ("mis solicitudes", "mi solicitudes", "mis tickets", "mi tickets", "mis requerimientos", "mi requerimientos", "historial", "seguimiento")):

                destino = "/usuario/mis-solicitudes" if "SOLICITANTE" in roles else ruta_inicio

                respuesta_navegacion = "Abriendo el seguimiento de tus solicitudes."

            elif any(x in texto for x in ("perfil", "mis datos", "mi cuenta")):

                destino = "/usuario/perfil"

                respuesta_navegacion = "Abriendo tu perfil."

            elif any(x in texto for x in ("notificaciones", "avisos")):

                destino = "/usuario/notificaciones" if "SOLICITANTE" in roles else ruta_inicio

                respuesta_navegacion = "Abriendo tus notificaciones."

            elif any(x in texto for x in ("compras", "compra", "almacen", "repuestos")):

                destino = {

                    "DAF": "/daf/dashboard", "TESORERIA": "/tesoreria/dashboard",

                    "ENCARGADO_COMPRAS_ALMACEN": "/almacen/dashboard",

                    "SOLICITANTE": "/usuario/compras",

                }.get(rol_principal, ruta_inicio)

                respuesta_navegacion = "Abriendo el módulo de compras."

            elif any(x in texto for x in ("soporte", "tickets", "ticket", "utic")):

                destino = {

                    "JEFE_UTIC": "/jefe-utic/dashboard", "ESPECIALISTA": "/especialista/dashboard",

                    "SOLICITANTE": "/usuario/soporte",

                }.get(rol_principal, ruta_inicio)

                respuesta_navegacion = "Abriendo soporte técnico."

            elif any(x in texto for x in ("mantenimiento", "infraestructura")):

                destino = {

                    "SERVICIOS_GENERALES": "/servicios-generales/dashboard",

                    "AUXILIAR_SERVICIOS_GENERALES": "/auxiliar-servicios-generales/dashboard",

                    "SOLICITANTE": "/usuario/mantenimiento",

                }.get(rol_principal, ruta_inicio)

                respuesta_navegacion = "Abriendo mantenimiento."

            if destino:

                return Response({

                    "respuesta": respuesta_navegacion,

                    "accion": {"tipo": "NAVEGACION", "ruta": destino},

                }, status=status.HTTP_200_OK)







        # ----------------------------------------------------------

        # 2. Obtener contexto del sistema para el usuario actual

        # ----------------------------------------------------------

        try:

            contexto = obtener_contexto(request.user)

        except Exception:

            # Si falla la consulta de contexto, continúa sin él

            contexto = "Contexto del sistema no disponible en este momento."



        # ----------------------------------------------------------

        # 3. Construir el prompt completo

        # ----------------------------------------------------------

        es_voz = str(request.data.get("modo", "")).strip().lower() == "voz"

        pantalla = str(request.data.get("pantalla", "") or "").strip()[:MAX_PANTALLA]



        bloque_pregunta = (

            f"=== PREGUNTA DEL USUARIO ===\n"

            f"{mensaje}\n"

            f"=== FIN DE PREGUNTA ==="

        )

        # Prompt original: lo usa el motor de respaldo (búsqueda por palabras clave),

        # sin instrucciones extra que puedan desviar la detección del tema.

        prompt = f"{contexto}\n\n{bloque_pregunta}"



        # Prompt para la IA: identidad de SIA-AI, pantalla actual y estilo hablado.

        # Orden pensado para la caché de Ollama: lo que casi no cambia va primero

        # (identidad, estilo, contexto); lo que cambia en cada pregunta, al final.

        partes = [INSTRUCCION_IDENTIDAD]

        if es_voz:

            partes.append(INSTRUCCION_VOZ)

        partes.append(contexto)

        if pantalla:

            partes.append(

                "=== PANTALLA QUE EL USUARIO ESTÁ VIENDO ===\n"

                f"{pantalla}\n"

                "=== FIN PANTALLA ==="

            )

        partes.append(bloque_pregunta)

        prompt_ia = "\n\n".join(partes)



        # ----------------------------------------------------------

        # 4. Consultar Ollama

        # ----------------------------------------------------------

        if request.data.get("stream"):

            return self._responder_por_partes(prompt_ia, prompt, es_voz)



        respuesta = consultar_ollama(prompt_ia, prompt_respaldo=prompt, voz=es_voz)



        # ----------------------------------------------------------

        # 5. Retornar respuesta

        # ----------------------------------------------------------

        return Response(

            {"respuesta": respuesta},

            status=status.HTTP_200_OK,

        )



    @staticmethod

    def _responder_por_partes(prompt_ia, prompt_respaldo, es_voz):

        """

        Respuesta en NDJSON (una línea JSON por trozo):

            {"delta": "texto parcial"} ... {"fin": true, "respuesta": "texto completo"}

        """

        def generar():

            partes = []

            for trozo in consultar_ollama_stream(prompt_ia, prompt_respaldo=prompt_respaldo, voz=es_voz):

                partes.append(trozo)

                yield json.dumps({"delta": trozo}, ensure_ascii=False) + "\n"

            yield json.dumps({"fin": True, "respuesta": "".join(partes).strip()}, ensure_ascii=False) + "\n"



        respuesta = StreamingHttpResponse(generar(), content_type="application/x-ndjson; charset=utf-8")

        respuesta["Cache-Control"] = "no-cache"

        respuesta["X-Accel-Buffering"] = "no"  # nginx: enviar cada trozo sin acumular

        return respuesta





# ==============================================================

# VOZ DE TATI (texto -> audio MP3, voz colombiana)

# ==============================================================



class VozTatiView(APIView):

    """

    POST /api/asistente/voz/

    Body JSON: { "texto": "frase a leer" }

    Respuesta: audio/mpeg  ·  503 si el servicio de voz no esta disponible

    (el frontend usa entonces la voz del navegador).

    """



    permission_classes = [IsAuthenticated]



    def post(self, request):

        texto = str(request.data.get("texto", "")).strip()

        if not texto:

            return Response({"error": "El campo 'texto' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        if len(texto) > voz.MAX_CARACTERES:

            return Response(

                {"error": f"El texto no puede superar los {voz.MAX_CARACTERES} caracteres."},

                status=status.HTTP_400_BAD_REQUEST,

            )

        try:

            audio = voz.sintetizar(texto)

        except voz.VozNoDisponible:

            return Response(

                {"error": "La voz de Tati no esta disponible en este momento."},

                status=status.HTTP_503_SERVICE_UNAVAILABLE,

            )

        respuesta = HttpResponse(audio, content_type="audio/mpeg")

        respuesta["Cache-Control"] = "private, max-age=86400"

        return respuesta

