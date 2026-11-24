# -*- coding: utf-8 -*-
"""
05_buscar_perfumes.py - Genera 05-buscar-perfumes.svg.

Ejecutar:  python 05_buscar_perfumes.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *


if __name__ == '__main__':
    b, h = catalog(True)
    PAGE('05-buscar-perfumes.svg', h, '5 · Buscar perfumes', 'Catálogo con una búsqueda y filtros aplicados.', b,
         ['Filtros activos como etiquetas que se pueden quitar una a una', 'Limpiar todo restablece el catálogo completo', 'La búsqueda se hace por nombre o marca',
          'Resultados paginados desde la API (/api/v1)'])
