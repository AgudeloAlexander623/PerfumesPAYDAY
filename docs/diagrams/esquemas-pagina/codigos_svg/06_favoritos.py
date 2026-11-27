# -*- coding: utf-8 -*-
"""
06_favoritos.py - Genera 06-favoritos.svg.

Ejecutar:  python 06_favoritos.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def favorites():
    b = NAV('', cart=2) + T(640, 140, 'Mis fragancias favoritas', 'h2', 'middle') + T(640, 170, 'Aquí está la lista de perfumes que guardaste para comprar después.', 'm', 'middle')
    for i in range(3): b += PCARD(140 + i * 350, 210, 300, 'fav')
    return b + FOOT(620), 790


if __name__ == '__main__':
    b, h = favorites()
    PAGE('06-favoritos.svg', h, '6 · Favoritos', 'Lista de perfumes guardados por el usuario.', b,
         ['El README deja fuera la lista de deseos (wishlist): confirmar con el líder', 'Si entra, requiere una tabla de favoritos por usuario',
          'Estado vacío: mensaje y botón para explorar el catálogo', 'La X quita el producto de la lista'])
