# -*- coding: utf-8 -*-
"""
01_inicio.py - Genera 01-inicio.svg.

Ejecutar:  python 01_inicio.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *


if __name__ == '__main__':
    b, h = home()
    PAGE('01-inicio.svg', h, '1 · Inicio', 'Página de inicio con hero, ventajas, pasos y catálogo destacado.', b,
         ['Navbar: Inicio, Catálogo y Mis pedidos; íconos de tema, búsqueda, favoritos, carrito y usuario', 'El ícono de usuario abre el menú (pantalla 8) o lleva al login si no hay sesión',
          'Mayoristas aparece como “Próximamente” (alcance de la beta)', 'Los datos del catálogo son marcadores: no hay marcas ni precios reales',
          'Aviso visible: simulador académico, sin cobros ni envíos reales', 'Responsive: en móvil el menú se colapsa'])
