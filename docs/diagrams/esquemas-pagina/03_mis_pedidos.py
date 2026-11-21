# -*- coding: utf-8 -*-
"""
03_mis_pedidos.py - Genera 03-mis-pedidos.svg.

Ejecutar:  python 03_mis_pedidos.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def orders():
    b = NAV('MIS PEDIDOS', cart=2) + T(640, 140, 'Historial de pedidos', 'h2', 'middle') + T(640, 168, 'Consulta el estado y los detalles de todas tus compras.', 'm', 'middle')
    b += R(140, 200, 1000, 150, 'card', 14)
    for x, l in ((170, 'ID PEDIDO'), (300, 'FECHA'), (520, 'MÉTODO DE PAGO'), (700, 'TOTAL'), (830, 'ESTADO'), (1010, 'ACCIÓN')): b += T(x, 240, l, 'hd')
    b += LN(160, 256, 1120, 256)
    for k, est in enumerate(('Pagado simulado', 'Cancelado')):
        y = 290 + 46 * k
        b += T(170, y, '#[ID]', 'tb') + T(300, y, '[FECHA Y HORA]', 't') + T(520, y, 'Pago simulado', 't') + T(700, y, '$[TOTAL]', 'tb gd')
        b += CHIP(830, y - 15, est)[0] + R(1010, y - 18, 100, 32, 'out', 6) + T(1060, y + 3, 'RASTREAR', 'bw', 'middle')
        if k == 0: b += LN(160, y + 22, 1120, y + 22)
    return b + FOOT(520), 690


if __name__ == '__main__':
    b, h = orders()
    PAGE('03-mis-pedidos.svg', h, '3 · Mis pedidos', 'Historial de pedidos del usuario autenticado.', b,
         ['Cada usuario solo ve sus propios pedidos (validado en el servidor)', 'Columnas según tabla pedidos: id, creado_en, total_cop y estado',
          'Método de pago: siempre “Pago simulado”', 'RASTREAR abre el detalle del pedido (pantalla 3.1)'])
