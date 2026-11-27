# -*- coding: utf-8 -*-
"""
04_cambiar_tema.py - Genera 04-cambiar-tema.svg.

Ejecutar:  python 04_cambiar_tema.py
(necesita comun.py en la misma carpeta; el SVG se guarda junto a este script)
"""
from comun import *


if __name__ == '__main__':
    b, h = home(sun=True)
    PAGE('04-cambiar-tema.svg', h, '4 · Cambiar tema', 'Inicio en tema claro tras pulsar el ícono de tema.', b,
         ['El ícono de la luna/sol alterna entre tema oscuro y claro', 'La preferencia se guarda en el navegador del usuario', 'Pantalla no incluida en el README: confirmar si entra en la beta'], 'light')
