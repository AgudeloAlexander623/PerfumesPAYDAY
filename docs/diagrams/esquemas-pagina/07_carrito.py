# -*- coding: utf-8 -*-
"""
07_carrito.py - Genera 07-carrito.svg.

Ejecutar:  python 07_carrito.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def cart():
    b = NAV('', 2) + T(640, 130, 'Mi carrito de compras', 'h2', 'middle') + T(640, 160, 'Revisa tus productos antes de continuar con la compra.', 'm', 'middle')
    for x, l in ((60, 'PRODUCTO'), (480, 'PRECIO UNITARIO'), (620, 'CANTIDAD'), (760, 'SUBTOTAL')): b += T(x, 236, l, 'hd')
    b += LN(60, 250, 880, 250)
    for k in range(2):
        y = 252 + 80 * k
        b += R(60, y + 14, 52, 52, 'ph', 6) + T(128, y + 34, '[MARCA]', 'up') + T(128, y + 56, '[NOMBRE DEL PERFUME] ([ml])', 'tb') + T(480, y + 46, '$[PRECIO]', 't')
        b += R(620, y + 25, 84, 30, 'inp', 6) + T(632, y + 46, '−', 't') + T(662, y + 46, '1', 't', 'middle') + T(692, y + 46, '+', 't', 'end') + T(760, y + 46, '$[SUBTOTAL]', 'tb')
        b += f'<path d="M852 {y + 36} h16 M854 {y + 36} v13 h12 v-13 M858 {y + 32} h4" class="glm"/>' + LN(60, y + 80, 880, y + 80)
    b += R(920, 230, 300, 340, 'card', 14) + T(944, 272, 'Resumen de compra', 'h3') + LN(944, 290, 1196, 290)
    b += T(944, 322, 'Subtotal', 'm') + T(1196, 322, '$[SUBTOTAL]', 'm', 'end') + T(944, 372, 'Total', 'h3 gd') + T(1196, 372, '$[TOTAL]', 'h3 gd', 'end')
    b += LN(944, 392, 1196, 392) + T(944, 420, 'Simulador académico: no se cobra', 'm') + T(944, 438, 'dinero real.', 'm')
    b += BTN(944, 462, 252, 48, 'CONTINUAR COMPRA') + BTNO(944, 520, 252, 44, 'SEGUIR COMPRANDO')
    return b + FOOT(800), 970


if __name__ == '__main__':
    b, h = cart()
    PAGE('07-carrito.svg', h, '7 · Carrito de compras', 'Carrito con tabla de productos y resumen.', b,
         ['Cantidad limitada por el stock disponible (controles + y −)', 'La papelera elimina el producto del carrito', 'Un carrito por usuario autenticado',
          'Total = suma de precio unitario x cantidad; sin costo de envío real', 'Estado vacío: “Tu carrito está vacío” y botón Explorar catálogo', 'Cupones: fuera del alcance de la beta'])
