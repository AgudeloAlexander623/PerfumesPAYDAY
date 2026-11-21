# -*- coding: utf-8 -*-
"""
08_usuario.py - Genera 08-usuario.svg.

Ejecutar:  python 08_usuario.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *


if __name__ == '__main__':
    b, h = home(menu=True, full=False)
    PAGE('08-usuario.svg', h, '8 · Usuario', 'Menú desplegable del usuario con sesión iniciada.', b,
         ['Muestra el nombre y el rol; opciones: Mi perfil, Mis pedidos y Cerrar sesión', 'Mi perfil abre la pantalla 8.1 (pendiente)',
          'Propuesta: si el rol es manager o admin, añadir “Panel de gestión”', 'Sin sesión, el ícono lleva al login'])
