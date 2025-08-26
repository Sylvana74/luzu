# ===================================

# controller/__init__.py
"""
Paquete Controller - Capa de Control
Contiene la lógica de negocio y coordinación entre Model y View
"""

from .cliente_controller import ClienteController

__all__ = ['ClienteController']