import re

from difflib import SequenceMatcher



from soporte.models import Ticket

from mantenimiento.models import RequerimientoMantenimiento



PALABRAS_VACIAS = {

    "a", "al", "algun", "alguna", "algunas", "algunos", "anda", "cada", "como",

    "con", "cual", "cuando", "cuanto", "cuantos", "cuantas", "dame", "dar", "de",

    "del", "desde", "detalle", "detalles",

    "dia", "dias", "el", "ella", "en", "es", "esta", "este", "fue", "hace", "hay",

    "informacion", "la", "las", "lo", "los", "mas", "me", "mi", "mis", "no",

    "para", "por", "porque", "favor", "que", "resumen", "resumir", "rato", "se",

    "si", "sobre", "tengo", "un", "una", "unas", "unos", "va", "yo",

}

PALABRAS_TIPO = {

    "ticket", "tickets", "soporte", "utic", "incidencia", "incidencias",

    "mantenimiento", "orden", "ordenes", "solicitud", "solicitudes",

    "requerimiento", "requerimientos", "pedido", "pedidos", "reporte", "reportes",

    "caso", "casos", "problema", "problemas", "condicion", "estado", "actual",

    "actualmente", "situacion", "funciona", "funcionar", "sirve", "falla", "fallo",

    "da", "mal", "mala", "malo",

}

ESTADOS_TICKET_EN_PROCESO = (

    "EN_PROCESO", "ASIGNADO", "EN_ANALISIS", "EN_EJECUCION", "EN_DIAGNOSTICO",

    "EN_VERIFICACION",

)

ESTADOS_MANTENIMIENTO_EN_PROCESO = (

    "DERIVADO", "EN_MANTENIMIENTO", "REVISION_ALMACEN", "EN_ESPERA_COMPRA",

)



def _normalizar(texto):

    texto = str(texto or "").casefold()

    texto = texto.translate(str.maketrans({

        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",

        "ü": "u", "ñ": "n",

    }))

    return re.sub(r"\s+", " ", texto).strip()





class ConsultasConversacionales:

    def __init__(self, usuario):

        self.usuario = usuario



    def _tickets(self):

        return Ticket.objects.filter(solicitante=self.usuario).select_related("estado", "categoria").order_by("-creado_en")



    def _mantenimientos(self):

        return RequerimientoMantenimiento.objects.filter(solicitante=self.usuario).select_related("estado").order_by("-creado_en")



    @staticmethod

    def _identificador(mensaje):

        codigo = re.search(r"\b[A-Z]{2,}-\d{4}-\d+\b", mensaje, re.IGNORECASE)

        if codigo:

            return "codigo", codigo.group().upper()

        numero = re.search(

            r"\b(?:solicitud|ticket|orden|requerimiento|mantenimiento|soporte|caso)"

            r"\s+(?:n(?:ro|umero)?\.?\s*)?(\d+)\b",

            _normalizar(mensaje),

        )

        if numero:

            return "numero", numero.group(1)

        numero = re.search(r"\b0\d{2,}\b", mensaje)

        return ("numero", numero.group()) if numero else None



    @staticmethod

    def _respuesta_detalle(tipo, objeto):

        codigo = getattr(objeto, "codigo", None) or f"{tipo}-{getattr(objeto, 'id', 'desconocido')}"

        titulo = str(getattr(objeto, "titulo", "") or "").strip()

        descripcion = str(getattr(objeto, "descripcion", "") or "").strip()

        estado = str(getattr(getattr(objeto, "estado", None), "nombre", "") or "").strip()

        ubicacion = str(getattr(objeto, "ubicacion", "") or "").strip()

        etiqueta = "soporte técnico" if tipo == "Ticket" else "mantenimiento"



        partes = [f"Solicitud de {etiqueta} {codigo}"]

        if titulo:

            partes[0] += f": {titulo}"

        partes[0] += "."

        if descripcion:

            resumen = descripcion if len(descripcion) <= 500 else descripcion[:497].rsplit(" ", 1)[0] + "..."

            partes.append(f"Resumen: {resumen}")

        partes.append(f"Estado actual: {estado or 'No disponible'}.")

        if ubicacion:

            partes.append(f"Ubicación: {ubicacion}.")

        return " ".join(partes)



    def _buscar_por_identificador(self, identificador, busca_ticket, busca_mantenimiento):

        tipo_id, valor = identificador

        tipos = []

        if busca_ticket and not busca_mantenimiento:

            tipos = [("Ticket", self._tickets())]

        elif busca_mantenimiento and not busca_ticket:

            tipos = [("Requerimiento", self._mantenimientos())]

        else:

            tipos = [("Ticket", self._tickets()), ("Requerimiento", self._mantenimientos())]



        for tipo, registros in tipos:

            if tipo_id == "codigo":

                objeto = registros.filter(codigo__iexact=valor).first()

            else:

                objeto = registros.filter(codigo__endswith=f"-{valor}").first()

                if objeto is None and len(valor) < 4:

                    objeto = registros.filter(codigo__endswith=f"-{valor.zfill(4)}").first()

            if objeto:

                return tipo, objeto

        return None



    @staticmethod

    def _es_conteo(texto):

        return bool(re.search(r"\b(?:cuant[oa]s?|cantidad|total|numero de)\b", texto))



    @staticmethod

    def _es_en_proceso(texto):

        return bool(re.search(

            r"\b(?:en (?:el )?(?:proceso|curso|ejecucion|atencion|marcha|reparacion)|"

            r"trabajando|atendiendose)\b",

            texto,

        ))



    @staticmethod

    def _es_reciente(texto):

        return bool(re.search(

            r"\b(?:ultim[oa]s?|recientes?|mas nuevo[as]?|mas recientes?|"

            r"que (?:registre|cree|hice|pedi|reporte))\b",

            texto,

        ))

    @staticmethod
    def _es_finalizado(texto):
        return bool(re.search(
            r"\b(?:finalizad[oa]s?|cerrad[oa]s?|concluid[oa]s?|terminad[oa]s?|resuelt[oa]s?)\b",
            texto,
        ))

    @staticmethod
    def _es_urgente(texto):
        return bool(re.search(
            r"\b(?:urgentes?|mas urgentes?|prioritari[oa]s?|mas prioritari[oa]s?|criticos?|criticas?|mas critic[oa]s?|mayor prioridad)\b",
            texto,
        ))



    @staticmethod

    def _puntaje(texto, registro):

        texto_registro = _normalizar(registro)

        palabras = {

            palabra for palabra in texto.split()

            if len(palabra) >= 3 and palabra not in PALABRAS_VACIAS and palabra not in PALABRAS_TIPO

        }

        if not palabras:

            return 0

        coincidencias = sum(

            1 for palabra in palabras

            if re.search(rf"\b{re.escape(palabra)}\b", texto_registro)

        )

        cobertura = coincidencias / len(palabras)

        secuencia = SequenceMatcher(None, texto, texto_registro).ratio()

        return max(secuencia, cobertura * (0.9 if len(palabras) > 1 else 0.65))



    def _obtener_mas_urgente(self, busca_ticket=True, busca_mantenimiento=True):
        candidatos = []
        peso_prioridad = {
            "CRITICA": 4, "URGENTE": 4,
            "ALTA": 3,
            "MEDIA": 2,
            "BAJA": 1,
        }

        # Tickets de soporte activos
        if busca_ticket or not busca_mantenimiento:
            activos_ticket = self._tickets().exclude(
                estado__codigo__in=("CERRADO", "RECHAZADO", "ANULADO", "CERRADO_SIN_COMPRA")
            )
            for t in activos_ticket:
                prio_str = (t.prioridad or "").upper()
                peso = peso_prioridad.get(prio_str, 0)
                candidatos.append({
                    "tipo": "ticket de soporte",
                    "codigo": t.codigo,
                    "titulo": t.titulo,
                    "prioridad": prio_str,
                    "peso": peso,
                    "estado": t.estado.nombre if t.estado else "Activo",
                    "creado_en": t.creado_en,
                    "sla": f"{t.sla_horas}h" if t.sla_horas else None,
                })

        # Requerimientos de mantenimiento activos
        if busca_mantenimiento or not busca_ticket:
            activos_mantenimiento = self._mantenimientos().exclude(
                estado__codigo__in=("FINALIZADO", "RECHAZADO", "ANULADO", "CERRADO_SIN_COMPRA")
            )
            for m in activos_mantenimiento:
                prio_str = (m.prioridad_jefatura or "").upper()
                peso = peso_prioridad.get(prio_str, 0)
                candidatos.append({
                    "tipo": "requerimiento de mantenimiento",
                    "codigo": m.codigo,
                    "titulo": m.titulo,
                    "prioridad": prio_str,
                    "peso": peso,
                    "estado": m.estado.nombre if m.estado else "Activo",
                    "creado_en": m.creado_en,
                    "sla": None,
                })

        if not candidatos:
            return None

        candidatos.sort(
            key=lambda c: (
                c["peso"],
                -(c["creado_en"].timestamp() if c.get("creado_en") else 0)
            ),
            reverse=True,
        )
        top = candidatos[0]

        if top["peso"] > 0:
            sla_txt = f" con SLA de {top['sla']}" if top["sla"] else ""
            return (
                f"Tu {top['tipo']} más urgente es el {top['codigo']} "
                f"(«{top['titulo']}»), clasificado con prioridad {top['prioridad']}{sla_txt} "
                f"y actualmente en estado «{top['estado']}»."
            )
        else:
            return (
                f"Tu {top['tipo']} activo más relevante es el {top['codigo']} "
                f"(«{top['titulo']}»), actualmente en estado «{top['estado']}» "
                f"(pendiente de clasificación de prioridad por jefatura)."
            )

    def buscar(self, mensaje, historial=None):

        texto = _normalizar(mensaje)

        if not texto:

            return None



        busca_ticket = any(x in texto for x in (

            "ticket", "soporte", "utic", "incidencia", "reporte", "computadora",

            "impresora", "internet", "wifi", "red", "laptop", "proyector",

        ))

        busca_mantenimiento = any(x in texto for x in (

            "mantenimiento", "orden", "aire", "puerta", "electricidad", "fuga",

            "infraestructura", "reparacion", "arreglo", "grifo", "techo",

        ))

        busca_solicitud_generica = any(x in texto for x in (

            "solicitud", "requerimiento", "pedido", "caso", "problema",

        )) or (

            self._es_reciente(texto)

            and any(x in texto for x in ("mi ", "mis ", "hice", "registre", "cree", "pedi", "solicite", "reporte"))

        )



        identificador = self._identificador(mensaje)

        if identificador:

            encontrado = self._buscar_por_identificador(

                identificador, busca_ticket, busca_mantenimiento,

            )

            if encontrado:

                return self._respuesta_detalle(*encontrado)

            tipo_id, valor = identificador

            return f"No encontré una solicitud tuya con el código o número {valor}."

        # Consulta de urgencia o máxima prioridad institucional
        if self._es_urgente(texto):
            urgente = self._obtener_mas_urgente(busca_ticket, busca_mantenimiento)
            if urgente:
                return urgente
            if busca_ticket and not busca_mantenimiento:
                return "No tienes tickets de soporte activos con prioridad asignada en este momento."
            if busca_mantenimiento and not busca_ticket:
                return "No tienes requerimientos de mantenimiento activos con prioridad asignada en este momento."
            return "No tienes solicitudes activas con prioridad asignada en este momento."

        if self._es_conteo(texto):
            # Conteo de solicitudes finalizadas / cerradas
            if self._es_finalizado(texto):
                conteo_ticket = 0
                conteo_mantenimiento = 0
                if busca_ticket or not busca_mantenimiento:
                    conteo_ticket = self._tickets().filter(
                        estado__codigo__in=("CERRADO", "RESUELTO", "CERRADO_SIN_COMPRA")
                    ).count()
                if busca_mantenimiento or not busca_ticket:
                    conteo_mantenimiento = self._mantenimientos().filter(
                        estado__codigo__in=("FINALIZADO", "CERRADO_SIN_COMPRA")
                    ).count()
                if busca_ticket and not busca_mantenimiento:
                    return f"Tienes {conteo_ticket} ticket(s) de soporte finalizado(s)."
                if busca_mantenimiento and not busca_ticket:
                    return f"Tienes {conteo_mantenimiento} requerimiento(s) de mantenimiento finalizado(s)."
                total = conteo_ticket + conteo_mantenimiento
                return (
                    f"Tienes {total} solicitud(es) finalizada(s) en total: "
                    f"{conteo_ticket} de soporte y {conteo_mantenimiento} de mantenimiento."
                )

            if self._es_en_proceso(texto):

                conteo_ticket = 0

                conteo_mantenimiento = 0

                if busca_ticket or not busca_mantenimiento:

                    conteo_ticket = self._tickets().filter(

                        estado__codigo__in=ESTADOS_TICKET_EN_PROCESO

                    ).count()

                if busca_mantenimiento or not busca_ticket:

                    conteo_mantenimiento = self._mantenimientos().filter(

                        estado__codigo__in=ESTADOS_MANTENIMIENTO_EN_PROCESO

                    ).count()

                if busca_ticket and not busca_mantenimiento:

                    return f"Tienes {conteo_ticket} ticket(s) de soporte en proceso."

                if busca_mantenimiento and not busca_ticket:

                    return f"Tienes {conteo_mantenimiento} requerimiento(s) de mantenimiento en proceso."

                total = conteo_ticket + conteo_mantenimiento

                return (

                    f"Tienes {total} solicitud(es) en proceso: "

                    f"{conteo_ticket} de soporte y {conteo_mantenimiento} de mantenimiento."

                )

            if busca_ticket:

                tickets = self._tickets()

                activos = tickets.exclude(estado__codigo__in=("CERRADO", "CERRADO_SIN_COMPRA", "CANCELADO"))

                return f"Tienes {activos.count()} ticket(s) de soporte activo(s)."

            if busca_mantenimiento:

                mantenimientos = self._mantenimientos()

                activos = mantenimientos.exclude(estado__codigo__in=("FINALIZADO", "CERRADO_SIN_COMPRA", "RECHAZADO", "ANULADO"))

                return f"Tienes {activos.count()} requerimiento(s) de mantenimiento activo(s)."

            if busca_solicitud_generica:

                tickets = self._tickets().exclude(estado__codigo__in=("CERRADO", "CERRADO_SIN_COMPRA", "CANCELADO"))

                mantenimientos = self._mantenimientos().exclude(

                    estado__codigo__in=("FINALIZADO", "CERRADO_SIN_COMPRA", "RECHAZADO", "ANULADO")

                )

                total = tickets.count() + mantenimientos.count()

                return f"Tienes {total} solicitud(es) activa(s) entre soporte y mantenimiento."



        if self._es_reciente(texto):

            objeto = None

            tipo = None

            if busca_mantenimiento:

                objeto = self._mantenimientos().first()

                tipo = "Requerimiento"

            elif busca_ticket:

                objeto = self._tickets().first()

                tipo = "Ticket"

            elif busca_solicitud_generica:

                ticket = self._tickets().first()

                mantenimiento = self._mantenimientos().first()

                if ticket and mantenimiento:

                    objeto, tipo = (

                        (ticket, "Ticket") if ticket.creado_en >= mantenimiento.creado_en

                        else (mantenimiento, "Requerimiento")

                    )

                elif ticket:

                    objeto, tipo = ticket, "Ticket"

                elif mantenimiento:

                    objeto, tipo = mantenimiento, "Requerimiento"

            if objeto:

                codigo = getattr(objeto, "codigo", f"{tipo}-{objeto.id}")

                estado = getattr(getattr(objeto, "estado", None), "nombre", "Sin estado")

                titulo = getattr(objeto, "titulo", "Sin título")

                return f"Tu {tipo.lower()} más reciente es {codigo}: {titulo}. Estado: {estado}."



        candidatos = []

        if busca_ticket or not busca_mantenimiento:

            for obj in self._tickets()[:30]:

                registro = " ".join((

                    getattr(obj, "codigo", ""),

                    getattr(obj, "titulo", ""),

                    getattr(obj, "descripcion", ""),

                ))

                coincidencia = self._puntaje(texto, registro)

                candidatos.append((coincidencia, "Ticket", obj))

        if busca_mantenimiento or not busca_ticket:

            for obj in self._mantenimientos()[:30]:

                registro = " ".join((

                    getattr(obj, "codigo", ""),

                    getattr(obj, "titulo", ""),

                    getattr(obj, "descripcion", ""),

                ))

                coincidencia = self._puntaje(texto, registro)

                candidatos.append((coincidencia, "Requerimiento", obj))



        candidatos.sort(key=lambda item: item[0], reverse=True)

        if candidatos and candidatos[0][0] >= 0.42:

            coincidencia, tipo, obj = candidatos[0]

            return self._respuesta_detalle(tipo, obj)

        return None

