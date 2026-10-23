"""Punto de compatibilidad para iniciar la interfaz principal."""

if __package__ in (None, ""):
    import os
    import sys

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from Interfaz.formularios import (
        FormularioBase,
        VentanaCliente,
        VentanaNuevaVenta,
        VentanaProducto,
        VentanaProveedor,
    )
    from Interfaz.ventana_principal import SistemaPanaderia, iniciar_interfaz
else:
    from .formularios import (
        FormularioBase,
        VentanaCliente,
        VentanaNuevaVenta,
        VentanaProducto,
        VentanaProveedor,
    )
    from .ventana_principal import SistemaPanaderia, iniciar_interfaz

__all__ = [
    "FormularioBase",
    "VentanaCliente",
    "VentanaNuevaVenta",
    "VentanaProducto",
    "VentanaProveedor",
    "SistemaPanaderia",
    "iniciar_interfaz",
]


if __name__ == "__main__":
    iniciar_interfaz()
