# -*- coding: utf-8 -*-
"""
login.py - Genera login.svg.

Ejecutar:  python login.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *

def auth(kind):
    b = NAV()
    if kind == 'login':
        b += R(420, 110, 440, 580, 'card', 14) + GEM(640, 160, 1.4) + T(640, 232, 'Iniciar sesión', 'h2', 'middle') + T(640, 260, 'Ingresa con tu cuenta de Perfumería Gold', 'm', 'middle')
        b += INP(460, 310, 360, 'Correo electrónico', 'correo@ejemplo.com') + INP(460, 396, 360, 'Contraseña', '••••••••') + T(802, 424, 'MOSTRAR', 'hd', 'end')
        b += R(460, 462, 360, 40, 'errb', 6) + T(640, 487, 'Credenciales inválidas (mensaje de error)', 'er', 'middle')
        b += BTN(460, 524, 360, 48, 'INICIAR SESIÓN') + TG(640, 614, '¿No tienes cuenta? ', 'Regístrate', '', 'm')
        return b, 760
    b += R(420, 100, 440, 710, 'card', 14) + GEM(640, 148, 1.4) + T(640, 216, 'Crear cuenta', 'h2', 'middle') + T(640, 244, 'Regístrate para armar tu carrito y comprar', 'm', 'middle')
    for i, (l, p) in enumerate([('Nombre completo', 'Nombre y apellido'), ('Correo electrónico', 'correo@ejemplo.com'), ('Teléfono (opcional)', '3000000000'), ('Contraseña', '••••••••'), ('Confirmar contraseña', '••••••••')]):
        b += INP(460, 292 + 78 * i, 360, l, p)
    b += BTN(460, 688, 360, 48, 'CREAR CUENTA') + TG(640, 772, '¿Ya tienes cuenta? ', 'Inicia sesión', '', 'm')
    return b, 840


if __name__ == '__main__':
    b, h = auth('login')
    PAGE('login.svg', h, 'L1 · Login', 'Inicio de sesión.', b,
         ['Campos: correo y contraseña', 'Validar formato del correo en cliente y servidor', 'Límite de intentos de inicio de sesión (rate limit)',
          'Error genérico: no revelar si el correo existe', 'Se emiten el token de acceso y el refresh token', 'Destino tras el login: por definir con el equipo'])
