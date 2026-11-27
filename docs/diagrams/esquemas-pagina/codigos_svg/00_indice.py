# -*- coding: utf-8 -*-
"""
00_indice.py - Genera 00-indice.svg.

Ejecutar:  python 00_indice.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def sitemap():
    b = ''
    def box(x, y, num, name, dashed=False):
        nb = len(num) * 8 + 16
        s = R(x, y, 156, 76, 'card', 10)
        if dashed: s += R(x, y, 156, 76, 'outgd', 10)
        return s + R(x + 10, y + 10, nb, 22, 'gold', 11) + T(x + 10 + nb / 2, y + 25, num, 'bk', 'middle') + T(x + 10, y + 60, name, 'tb2')
    b += box(562, 40, '0', 'Inicio') + LN(640, 116, 640, 150, 'ar') + LN(118, 150, 1162, 150, 'ar')
    row = [('2', 'Catálogo', 0), ('3', 'Mis pedidos', 0), ('4', 'Cambiar tema', 0), ('5', 'Buscar perfumes', 0), ('6', 'Favoritos', 1), ('7', 'Carrito', 0), ('8', 'Usuario', 0)]
    for i, (n, nm, d) in enumerate(row):
        x = 40 + i * 174
        b += LN(x + 78, 150, x + 78, 188, 'ar', True) + box(x, 190, n, nm, d)
    b += LN(292, 266, 292, 338, 'ar', True) + box(214, 340, '3.1', 'Rastrear pedido', True)
    b += LN(292, 416, 292, 448, 'ar', True) + box(214, 450, '3.1.1', 'Factura pedido', True)
    b += LN(1162, 266, 1162, 338, 'ar', True) + box(1084, 340, '8.1', 'Mi perfil')
    b += LN(1084, 378, 1075, 378) + LN(1075, 378, 1075, 668)
    for y, n, nm in ((450, '8.1.1', 'Historial pedidos'), (540, '8.1.2', 'Libreta direcciones'), (630, '8.1.3', 'Datos personales')):
        b += LN(1075, y + 38, 1082, y + 38, 'ar', True) + box(1084, y, n, nm)
    b += T(40, 700, 'AUTENTICACIÓN (USUARIO SIN SESIÓN)', 'up') + box(40, 716, 'L1', 'Login') + box(214, 716, 'L2', 'Registro')
    b += R(640, 740, 156, 40, 'outgd', 10) + T(812, 765, 'Fuera del alcance actual del README: confirmar', 'm')
    return b, 830


if __name__ == '__main__':
    b, h = sitemap()
    PAGE('00-indice.svg', h, '0 · Índice de pantallas', 'Mapa de navegación entre las pantallas del proyecto.', b,
         ['Cada número corresponde a un SVG de esta carpeta (misma numeración del draw.io)', 'Las flechas indican la navegación desde menú, botones o íconos',
          'Borde punteado: pantallas fuera del alcance actual del README (confirmar con el líder)', 'L1 y L2 (login y registro) se abren desde el ícono de usuario sin sesión'])
