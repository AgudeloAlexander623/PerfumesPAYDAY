# -*- coding: utf-8 -*-
"""
02_catalogo.py - Genera 02-catalogo.svg.

Ejecutar:  python 02_catalogo.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *


if __name__ == '__main__':
    b, h = catalog(False)
    PAGE('02-catalogo.svg', h, '2 · Catálogo', 'Listado de fragancias con filtros laterales.', b,
         ['Filtros: búsqueda, género, marca, familia olfativa, presentación y precio', 'Solo se listan productos y presentaciones activos',
          'El precio mostrado es el de la presentación más económica', 'La disponibilidad sale del inventario (stock)',
          'El corazón agrega a favoritos (pantalla 6, por confirmar)', 'El botón de carrito agrega la presentación al carrito del usuario'])
