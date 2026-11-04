"""
asistente/contexto.py

Extrae información operativa real del sistema SIGTA desde la base
de datos mediante el ORM de Django, y la formatea como texto para
inyectarla al prompt de Ollama.

El contexto incluye:
  - Nombre y rol(es) del usuario autenticado
  - Área asignada
  - Sus tickets/órdenes activas más recientes
"""

from usuarios.models import UsuarioRol


# ==============================================================
# CONSULTAS ORM
# ==============================================================

def _obtener_roles(usuario) -> list[str]:
    """Retorna la lista de nombres de roles activos del usuario."""
    return list(
        UsuarioRol.objects
        .filter(usuario=usuario, activo=True)
        .select_related("rol")
        .values_list("rol__nombre", flat=True)
    )


def _obtener_area(usuario) -> str:
    """Retorna el nombre del área del usuario, o 'Sin área asignada'."""
    rol_con_area = (
        UsuarioRol.objects
        .filter(usuario=usuario, activo=True, area__isnull=False)
        .select_related("area")
        .first()
    )
    if rol_con_area and rol_con_area.area:
        return rol_con_area.area.nombre
    return "Sin área asignada"


def _obtener_tickets_activos(usuario) -> list[dict]:
    """
    Retorna los últimos 5 tickets de soporte activos del usuario.
    Compatible tanto si es solicitante como si es técnico asignado.
    """
    try:
        from soporte.models import Ticket
        tickets = (
            Ticket.objects
            .filter(solicitante=usuario)
            .exclude(estado__in=["CERRADO", "CANCELADO"])
            .order_by("-creado_en")
            .values("id", "estado", "descripcion")[:5]
        )
        return list(tickets)
    except Exception:
        return []


def _obtener_ordenes_mantenimiento(usuario) -> list[dict]:
    """
    Retorna las últimas 5 órdenes de mantenimiento activas
    relacionadas con el usuario (como solicitante o técnico).
    """
    try:
        from mantenimiento.models import RequerimientoMantenimiento
        ordenes = (
            RequerimientoMantenimiento.objects
            .filter(solicitante=usuario)
            .exclude(estado__in=["CERRADO", "CANCELADO"])
            .order_by("-creado_en")
            .values("id", "estado", "descripcion")[:5]
        )
        return list(ordenes)
    except Exception:
        return []


# ==============================================================
# FUNCIÓN PRINCIPAL
# ==============================================================

def obtener_contexto(usuario) -> str:
    """
    Construye el bloque de contexto operativo del usuario
    para inyectar en el prompt de Ollama.

    Parámetros:
        usuario: Instancia del modelo Usuario autenticado.

    Retorna:
        str: Texto con la información del usuario y su estado
             en el sistema, listo para incluir en el prompt.
    """
    roles = _obtener_roles(usuario)
    area = _obtener_area(usuario)
    tickets = _obtener_tickets_activos(usuario)
    ordenes = _obtener_ordenes_mantenimiento(usuario)

    lineas = [
        "=== CONTEXTO DEL USUARIO ACTUAL ===",
        f"Nombre: {usuario.nombre_completo}",
        f"Correo: {usuario.email}",
        f"Roles en el sistema: {', '.join(roles) if roles else 'Sin roles asignados'}",
        f"Área: {area}",
    ]

    if tickets:
        lineas.append(f"Tickets de soporte activos ({len(tickets)}):")
        for t in tickets:
            estado = t.get("estado", "")
            desc = str(t.get("descripcion", ""))[:80]
            lineas.append(f"  - ID {t['id']} | {estado} | {desc}")
    else:
        lineas.append("Tickets de soporte activos: ninguno.")

    if ordenes:
        lineas.append(f"Órdenes de mantenimiento activas ({len(ordenes)}):")
        for o in ordenes:
            estado = o.get("estado", "")
            desc = str(o.get("descripcion", ""))[:80]
            lineas.append(f"  - ID {o['id']} | {estado} | {desc}")
    else:
        lineas.append("Órdenes de mantenimiento activas: ninguna.")

    lineas.append("=== FIN DE CONTEXTO ===")

    return "\n".join(lineas)
