"""
Mongo document structure/constants for Locales.
"""

LOCALES_COLLECTION = "locales"

STATUS_DISPONIBLE = "disponible"
STATUS_OCUPADO = "ocupado"
STATUS_MANTENIMIENTO = "mantenimiento"

ALLOWED_STATUS = {STATUS_DISPONIBLE, STATUS_OCUPADO, STATUS_MANTENIMIENTO}
