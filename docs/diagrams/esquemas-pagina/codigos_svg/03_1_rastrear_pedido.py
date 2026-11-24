# -*- coding: utf-8 -*-
"""
03_1_rastrear_pedido.py - Genera 03-1-rastrear-pedido.svg.

Ejecutar:  python 03_1_rastrear_pedido.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def tracking():
    b = NAV('MIS PEDIDOS', cart=2) + BTNO(940, 90, 200, 34, '← VOLVER A MIS PEDIDOS')
    b += R(140, 150, 1000, 84, 'card', 14) + T(166, 188, 'Pedido #[ID]', 'h3') + T(166, 212, 'Realizado el [FECHA Y HORA]', 'm')
    b += BTNO(900, 176, 150, 32, 'IMPRIMIR RECIBO') + T(1100, 197, 'Pagado', 't', 'middle')
    b += R(140, 254, 1000, 170, 'card', 14) + T(166, 290, 'Estado del pedido', 'h3') + LN(200, 340, 1080, 340)
    for i, lab in enumerate(('Pendiente', 'Pagado', 'Preparando', 'Enviado', 'Entregado')):
        x = 200 + i * 220
        b += f'<circle cx="{x}" cy="340" r="18" class="{"gold" if i == 1 else "ic"}"/>' + T(x, 380, lab, 'tb2' if i == 1 else 'm', 'middle')
    b += R(140, 444, 1000, 190, 'card', 14) + T(166, 480, 'Productos comprados', 'h3') + LN(160, 498, 1120, 498)
    for x, l, a in ((170, 'PRODUCTO', 'start'), (560, 'PRECIO UNITARIO', 'start'), (760, 'CANTIDAD', 'start'), (1110, 'TOTAL', 'end')): b += T(x, 522, l, 'hd', a)
    b += LN(160, 534, 1120, 534) + T(170, 570, '[NOMBRE DEL PERFUME] · [MARCA] · [ml]', 't') + T(560, 570, '$[PRECIO]', 't') + T(760, 570, '[N]', 't') + T(1110, 570, '$[TOTAL]', 'tb', 'end')
    return b + FOOT(700), 870


if __name__ == '__main__':
    b, h = tracking()
    PAGE('03-1-rastrear-pedido.svg', h, '3.1 · Rastrear pedido', 'Detalle de un pedido con su línea de estado.', b,
         ['Hoy la base solo tiene los estados pagado_simulado y cancelado: la línea de 5 pasos requiere ampliarlos', 'El README deja fuera transportadoras y envíos reales (confirmar si se mantiene)',
          'Productos desde items_pedido: copia del nombre, marca, tamaño y precio al comprar', 'IMPRIMIR RECIBO abre la pantalla 3.1.1'])
