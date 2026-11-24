# -*- coding: utf-8 -*-
"""
03_1_1_factura_pedido.py - Genera 03-1-1-factura-pedido.svg.

Ejecutar:  python 03_1_1_factura_pedido.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def invoice():
    b = BTNO(140, 50, 200, 40, '← VOLVER AL PEDIDO') + BTN(900, 50, 240, 40, 'IMPRIMIR RECIBO')
    b += R(140, 120, 1000, 740, 'card', 14) + T(180, 190, 'PERFUMERÍA GOLD', 'h2') + T(180, 218, 'Tienda online de perfumes · Proyecto académico', 'm')
    b += T(1100, 190, 'RECIBO DE VENTA', 'h2 gd', 'end') + T(1100, 222, 'Pedido ID: #[ID]', 'tb', 'end') + T(1100, 246, 'Fecha de emisión: [FECHA]', 't', 'end') + T(1100, 270, 'Método de pago: Simulado', 't', 'end')
    b += LN(180, 300, 1100, 300) + T(180, 340, 'ENTREGAR A', 'up') + T(600, 340, 'DETALLES DE ENVÍO', 'up')
    for i, (l, v) in enumerate((('Cliente: ', '[NOMBRE DESTINATARIO]'), ('Teléfono: ', '[TELÉFONO]'), ('Correo: ', '[CORREO]'))): b += T(180, 376 + 28 * i, l + v, 't')
    for i, (l, v) in enumerate((('Dirección: ', '[DIRECCIÓN]'), ('Destino: ', '[CIUDAD], [DEPARTAMENTO]'), ('Estado del pedido: ', '[ESTADO]'))): b += T(600, 376 + 28 * i, l + v, 't')
    b += R(180, 480, 920, 44, 'inp', 4)
    for x, l, a in ((200, 'FRAGANCIA', 'start'), (560, 'PRESENTACIÓN', 'start'), (700, 'CANTIDAD', 'start'), (900, 'PRECIO UNITARIO', 'end'), (1080, 'SUBTOTAL', 'end')): b += T(x, 508, l, 'hd', a)
    b += T(200, 560, '[NOMBRE DEL PERFUME] · [MARCA]', 'tb') + T(560, 560, '[ml]', 't') + T(700, 560, '[N]', 't') + T(900, 560, '$[PRECIO]', 't', 'end') + T(1080, 560, '$[SUBTOTAL]', 'tb', 'end') + LN(180, 584, 1100, 584)
    b += T(880, 640, 'Subtotal:', 't', 'end') + T(1080, 640, '$[SUBTOTAL]', 'tb', 'end') + T(880, 690, 'Total general:', 'h3 gd', 'end') + T(1080, 690, '$[TOTAL]', 'h3 gd', 'end')
    b += LN(180, 760, 1100, 760) + T(640, 798, '¡Gracias por tu compra en Perfumería Gold!', 't', 'middle') + T(640, 822, 'Documento simulado: no es una factura electrónica ni tiene validez tributaria.', 'm', 'middle')
    return b, 900


if __name__ == '__main__':
    b, h = invoice()
    PAGE('03-1-1-factura-pedido.svg', h, '3.1.1 · Factura (recibo) del pedido', 'Recibo imprimible del pedido en tema claro.', b,
         ['Es un recibo simulado: la facturación electrónica DIAN está fuera del alcance', 'Dirección y destinatario salen de las columnas envio_* de pedidos',
          'El correo no se guarda en pedidos: tomarlo del usuario o quitar el campo', 'Tema claro pensado para imprimir o guardar como PDF'], 'light')
