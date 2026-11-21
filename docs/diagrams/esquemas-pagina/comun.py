# -*- coding: utf-8 -*-
"""
comun.py - Estilos y piezas reutilizables de los esquemas de Perfumería Gold.

No se ejecuta solo: lo importa cada script de pantalla (00_indice.py, 01_inicio.py, ...).
Aquí están los colores (PAL), el menú (NAV), el pie (FOOT), las tarjetas de producto
(PCARD) y las pantallas compartidas: home() y catalog().
"""
import os, sys, math, xml.dom.minidom

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(sys.argv[0]))
os.makedirs(OUT, exist_ok=True)
W = 1280

# ----------------------------------------------------------------- estilos
PAL = {
 'dark':  dict(BG='#0C0C12', CARD='#15151D', LINE='#2A2A35', TEXT='#FFFFFF', MUTED='#9CA3AF', INP='#0C0C12',
               IC='#1B1B24', OUT='#3A3A48', GT='#E0B02B', PH='#E5E7EB', NOTEBG='#101017', NOTET='#D1D5DB'),
 'light': dict(BG='#F3F4F6', CARD='#FFFFFF', LINE='#E5E7EB', TEXT='#111827', MUTED='#6B7280', INP='#FFFFFF',
               IC='#EDEDF1', OUT='#9CA3AF', GT='#B7791F', PH='#D1D5DB', NOTEBG='#FFFFFF', NOTET='#374151'),
}
CSS = '''<style>
text{font-family:"Plus Jakarta Sans",Outfit,Arial,Helvetica,sans-serif;fill:@TEXT}
.h1{font-size:48px;font-weight:700}
.h2{font-size:30px;font-weight:700}
.h3{font-size:18px;font-weight:700}
.t{font-size:15px}
.tb{font-size:15px;font-weight:700}
.tb2{font-size:13px;font-weight:700}
.st{font-size:16px;fill:@MUTED}
.m{font-size:13px;fill:@MUTED}
.lb{font-size:13px;font-weight:700}
.gd{fill:@GT}
.up{font-size:12px;font-weight:700;fill:@GT;letter-spacing:1px}
.hd{font-size:11px;font-weight:700;fill:@MUTED;letter-spacing:1px}
.nv{font-size:13px;font-weight:700;letter-spacing:.5px}
.bk{font-size:14px;font-weight:700;fill:#14110A;letter-spacing:1px}
.bw{font-size:13px;font-weight:700;letter-spacing:1px}
.bd{font-size:10px;font-weight:700;fill:#14110A}
.er{font-size:13px;fill:#FCA5A5}
.rd{font-size:13px;fill:#F87171}
.nt{font-size:13px;fill:@NOTET}
.card{fill:@CARD;stroke:@LINE;stroke-width:1}
.inp{fill:@INP;stroke:@LINE;stroke-width:1}
.chk{fill:@INP;stroke:@OUT;stroke-width:1.2}
.gold{fill:#E0B02B}
.out{fill:none;stroke:@OUT;stroke-width:1.5}
.outg{fill:none;stroke:@GT;stroke-width:1}
.outgd{fill:none;stroke:@GT;stroke-width:1.5;stroke-dasharray:6 4}
.errb{fill:#2A1518;stroke:#7F1D1D;stroke-width:1}
.ln{stroke:@LINE;stroke-width:1}
.lng{stroke:#E0B02B;stroke-width:2}
.ar{stroke:#E0B02B;stroke-width:1.5;fill:none}
.ph{fill:@PH}
.phx{stroke:#9CA3AF;stroke-width:1}
.chip{fill:@IC;stroke:@LINE;stroke-width:1}
.ic{fill:@IC;stroke:@LINE;stroke-width:1}
.gl{fill:none;stroke:@TEXT;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.glm{fill:none;stroke:@MUTED;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.glk{fill:none;stroke:#14110A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.glg{fill:none;stroke:#E0B02B;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.hf{fill:#E0B02B}
.note{fill:@NOTEBG;stroke:@OUT;stroke-width:1;stroke-dasharray:6 4}
</style>'''
DEFS = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        '<path d="M2 1L8 5L2 9" fill="none" stroke="#E0B02B" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')

# --------------------------------------------------------------- utilidades
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def R(x, y, w, h, c, rx=8): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{c}"/>'
def T(x, y, s, c='t', a='start'): return f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}">{esc(s)}</text>'
def TG(x, y, pre, gold, post, c='t', a='middle'):
    return f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}">{esc(pre)}<tspan class="gd">{esc(gold)}</tspan>{esc(post)}</text>'
def LN(x1, y1, x2, y2, c='ln', arrow=False):
    m = ' marker-end="url(#ar)"' if arrow else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{c}"{m}/>'
def BTN(x, y, w, h, label): return R(x, y, w, h, 'gold', 6) + T(x + w / 2, y + h / 2 + 5, label, 'bk', 'middle')
def BTNO(x, y, w, h, label): return R(x, y, w, h, 'out', 6) + T(x + w / 2, y + h / 2 + 5, label, 'bw', 'middle')
def CHIP(x, y, label, c='chip'):
    w = int(len(label) * 6.6 + 20)
    return R(x, y, w, 22, c, 5) + T(x + w / 2, y + 15, label, 'm', 'middle'), w
def IMG(x, y, w, h): return R(x, y, w, h, 'ph', 6) + LN(x, y, x + w, y + h, 'phx') + LN(x + w, y, x, y + h, 'phx')
def INP(x, y, w, label, ph, h=46):
    return T(x, y - 9, label, 'lb') + R(x, y, w, h, 'inp') + T(x + 16, y + h / 2 + 5, ph, 'm')
def GEM(cx, cy, k=1.0):
    p = ' '.join(f'{cx + a * k:.1f},{cy + b * k:.1f}' for a, b in [(-9, -7), (9, -7), (14, -1), (0, 12), (-14, -1)])
    return f'<polygon points="{p}" class="gl"/>'
def HEART(cx, cy, c='hf'):
    return f'<path transform="translate({cx} {cy})" d="M0,-4 C-2,-8 -8,-7 -8,-2 C-8,2 -3,5 0,8 C3,5 8,2 8,-2 C8,-7 2,-8 0,-4 Z" class="{c}"/>'
def BAG(x, y, c='glk'):
    return f'<rect x="{x}" y="{y + 3}" width="14" height="11" rx="3" class="{c}"/><path d="M{x + 4} {y + 3} v-2 a3 3 0 0 1 6 0 v2" class="{c}"/>'
def CHECK(x, y, label, on=False):
    s = R(x, y, 14, 14, 'gold' if on else 'chk', 3)
    if on: s += f'<path d="M{x + 3} {y + 7} l3 3 l5 -6" class="glk"/>'
    return s + T(x + 24, y + 12, label, 'm')

def NAV(active=None, cart=0, sun=False, menu=False):
    s = GEM(152, 32) + T(182, 38, 'PERFUMERÍA GOLD', 'h3')
    for lab, x in (('INICIO', 520), ('CATÁLOGO', 610), ('MIS PEDIDOS', 720)):
        s += T(x, 37, lab, 'nv')
        if lab == active: s += LN(x, 46, x + len(lab) * 8.6, 46, 'lng')
    for cx in (940, 988, 1036, 1084, 1132): s += f'<circle cx="{cx}" cy="32" r="18" class="ic"/>'
    if sun:
        s += '<circle cx="940" cy="32" r="18" class="outg"/><circle cx="940" cy="32" r="4" class="gl"/>'
        for k in range(8):
            a = k * math.pi / 4
            s += LN(f'{940 + 7 * math.cos(a):.1f}', f'{32 + 7 * math.sin(a):.1f}', f'{940 + 10 * math.cos(a):.1f}', f'{32 + 10 * math.sin(a):.1f}', 'gl')
    else:
        s += '<path d="M943 25 A8 8 0 1 0 947 35 A6 6 0 0 1 943 25 Z" class="gl"/>'
    s += '<circle cx="986" cy="30" r="6" class="gl"/>' + LN(990, 34, 995, 39, 'gl') + HEART(1036, 32) + BAG(1077, 25, 'gl')
    s += '<circle cx="1132" cy="28" r="4" class="gl"/><path d="M1124 41 Q1132 31 1140 41" class="gl"/>'
    if menu: s += '<circle cx="1132" cy="32" r="18" class="outg"/>'
    if cart: s += '<circle cx="1092" cy="18" r="8" class="gold"/>' + T(1092, 21.5, str(cart), 'bd', 'middle')
    return s + LN(0, 64, W, 64)

def FOOT(y):
    s = LN(0, y, W, y) + T(140, y + 44, 'PERFUMERÍA GOLD', 'h3 gd')
    for i, l in enumerate(['Perfumes para explorar, elegir y', 'comprar. Proyecto académico: no se', 'cobra ni se envían productos reales.']): s += T(140, y + 72 + 20 * i, l, 'm')
    s += T(540, y + 44, 'Navegación', 'h3 gd')
    for i, l in enumerate(['Inicio', 'Catálogo', 'Mis pedidos']): s += T(540, y + 72 + 22 * i, l, 'm')
    s += T(780, y + 44, 'Atención al cliente', 'h3 gd')
    for i, l in enumerate(['Mi cuenta', 'Mis pedidos', 'Carrito de compras']): s += T(780, y + 72 + 22 * i, l, 'm')
    return s

def NOTES(y, title, lines):
    rows = math.ceil(len(lines) / 2); h = 60 + 24 * rows
    s = f'<rect x="40" y="{y}" width="1200" height="{h}" rx="10" class="note"/>' + T(64, y + 34, 'Notas · ' + title, 'h3')
    for i, l in enumerate(lines): s += T(64 + (i // rows) * 580, y + 66 + 24 * (i % rows), '• ' + l, 'nt')
    return s, h

def PAGE(name, sh, title, desc, body, notes, theme='dark'):
    p = PAL[theme]; css = CSS
    for k, v in p.items(): css = css.replace('@' + k, v)
    ns, nh = NOTES(sh + 30, title, notes); H = sh + 30 + nh + 30
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
           f'<title>{esc(title)}</title><desc>{esc(desc)}</desc>{DEFS}{css}<rect width="{W}" height="{H}" fill="{p["BG"]}"/>'
           f'{body}{LN(0, sh, W, sh)}{ns}</svg>')
    xml.dom.minidom.parseString(svg)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg)
    print('OK ', name)

def PCARD(x, y, w, mode='cat'):
    s = R(x, y, w, 330, 'card', 14) + IMG(x + 20, y + 20, w - 40, 150) + T(x + 20, y + 198, '[MARCA]', 'up') + T(x + 20, y + 222, '[NOMBRE DEL PERFUME]', 'tb')
    c1, w1 = CHIP(x + 20, y + 236, '[Género]'); c2, _ = CHIP(x + 28 + w1, y + 236, '[Familia]')
    s += c1 + c2 + LN(x + 20, y + 274, x + w - 20, y + 274) + T(x + 20, y + 308, '$[PRECIO]', 'h3')
    s += R(x + w - 54, y + 284, 34, 34, 'gold', 6) + BAG(x + w - 44, y + 292)
    if mode == 'fav':
        s += R(x + w - 52, y + 28, 32, 32, 'card', 6) + HEART(x + w - 36, y + 44)
        s += R(x + w - 96, y + 284, 34, 34, 'out', 6) + f'<path d="M{x + w - 85} {y + 295} l12 12 M{x + w - 73} {y + 295} l-12 12" class="glm"/>'
    else:
        s += R(x + w - 96, y + 284, 34, 34, 'out', 6) + HEART(x + w - 79, y + 301, 'glm')
    return s


def home(menu=False, sun=False, full=True):
    b = NAV('INICIO', cart=0, sun=sun, menu=menu)
    b += R(0, 65, W, 430, 'card', 0) + T(1240, 92, '[IMAGEN DE FONDO DEL HERO]', 'm', 'end')
    b += R(520, 150, 240, 28, 'outg', 14) + T(640, 169, 'TIENDA ONLINE DE PERFUMES', 'up', 'middle')
    b += T(640, 250, 'Explora, elige y compra', 'h1', 'middle') + TG(640, 310, 'tu ', 'próxima', '  fragancia', 'h1')
    b += T(640, 356, 'Regístrate, arma tu carrito y simula tu compra en una', 'st', 'middle') + T(640, 380, 'experiencia inspirada en MercadoLibre.', 'st', 'middle')
    b += BTN(470, 416, 170, 48, 'VER CATÁLOGO') + BTNO(660, 416, 170, 48, 'CREAR CUENTA')
    b += R(140, 520, 1000, 90, 'card', 14)
    for i, (a, c) in enumerate([('PRESENTACIONES', '30, 50 y 100 ml'), ('CARRITO PROPIO', 'Uno por cada usuario'), ('COMPRA SIMULADA', 'Sin cobros reales'), ('HISTORIAL', 'Todos tus pedidos')]):
        x = 140 + i * 250
        if i: b += LN(x, 540, x, 590)
        b += f'<circle cx="{x + 40}" cy="565" r="18" class="ic"/><circle cx="{x + 40}" cy="565" r="5" class="glg"/>' + T(x + 68, 561, a, 'lb') + T(x + 68, 580, c, 'm')
    if menu:
        b += R(960, 58, 200, 170, 'card', 10) + T(978, 86, 'Hola, [NOMBRE]', 'tb') + CHIP(978, 96, 'CLIENTE', 'outg')[0].replace('class="outg"', 'class="outg"')
        b += LN(960, 132, 1160, 132)
        for i, (l, c) in enumerate([('Mi perfil', 'm'), ('Mis pedidos', 'm'), ('Cerrar sesión', 'rd')]): b += T(978, 160 + 26 * i, l, c)
    if not full: return b, 640
    b += T(640, 676, 'CÓMO FUNCIONA', 'up', 'middle') + T(640, 716, 'Comprar en cuatro pasos', 'h2', 'middle')
    for i, (a, c) in enumerate([('Regístrate', 'Crea tu cuenta e inicia sesión'), ('Explora', 'Filtra por marca, género y familia'), ('Arma tu carrito', 'Elige 30, 50 o 100 ml'), ('Simula tu compra', 'Guarda tu dirección y confirma')]):
        x = 140 + i * 250
        b += f'<circle cx="{x + 22}" cy="780" r="22" class="gold"/>' + T(x + 22, 786, str(i + 1), 'bk', 'middle') + T(x, 836, a, 'h3') + T(x, 860, c, 'm')
    b += T(140, 940, 'CATÁLOGO DESTACADO', 'up') + T(140, 978, 'Fragancias para elegir', 'h2')
    for i in range(3): b += PCARD(140 + i * 350, 1010, 300)
    b += R(140, 1430, 1000, 120, 'card', 14) + T(640, 1480, 'VENTAS AL POR MAYOR', 'up', 'middle') + T(640, 1524, 'Próximamente', 'h2', 'middle')
    return b + FOOT(1590), 1760

def catalog(filtered):
    b = NAV('CATÁLOGO', cart=2)
    b += R(140, 100, 1000, 140, 'card', 16) + T(170, 142, 'CATÁLOGO', 'up') + T(170, 182, 'Explora nuestras fragancias', 'h2')
    b += T(170, 212, 'Filtra por marca, género y familia olfativa para encontrar tu aroma.', 'm')
    top = 270
    if filtered:
        b += T(140, 292, 'FILTROS ACTIVOS', 'hd'); x = 260
        for lab in ('Género: Hombre  ×', 'Marca: [MARCA 1]  ×', 'Presentación: 100 ml  ×', 'Precio: [Mín] - [Máx]  ×'):
            c, w = CHIP(x, 276, lab, 'outg'); b += c; x += w + 10
        b += T(x + 6, 292, 'Limpiar todo', 'm').replace('class="m"', 'class="m gd"')
        top = 324
    b += R(140, top, 240, 800, 'card', 14) + T(160, top + 36, 'Buscar', 'h3')
    b += R(160, top + 50, 200, 38, 'inp', 6) + T(176, top + 74, '[texto buscado]' if filtered else 'Nombre o marca...', 'm')
    blocks = [('Género', ['Hombre', 'Mujer', 'Unisex'], 0), ('Marcas', ['[MARCA 1]', '[MARCA 2]', '[MARCA 3]'], 0 if not filtered else 0),
              ('Familia olfativa', ['[FAMILIA 1]', '[FAMILIA 2]', '[FAMILIA 3]'], None), ('Presentación', ['30 ml', '50 ml', '100 ml'], 2)]
    yy = top + 124
    for name, items, on in blocks:
        b += LN(160, yy - 16, 360, yy - 16) + T(160, yy + 10, name, 'h3')
        for i, it in enumerate(items): b += CHECK(160, yy + 30 + 26 * i, it, filtered and on == i)
        yy += 124
    b += LN(160, yy - 16, 360, yy - 16) + T(160, yy + 10, 'Precio (COP)', 'h3')
    b += R(160, yy + 26, 90, 34, 'inp', 6) + T(172, yy + 48, 'Mín', 'm') + R(270, yy + 26, 90, 34, 'inp', 6) + T(282, yy + 48, 'Máx', 'm')
    b += BTN(160, top + 702, 200, 40, 'APLICAR FILTROS') + BTNO(160, top + 750, 200, 38, 'LIMPIAR FILTROS')
    b += R(400, top, 740, 56, 'card', 12) + T(420, top + 34, 'Se encontraron [N] fragancias', 'm')
    b += R(960, top + 10, 160, 36, 'inp', 6) + T(976, top + 33, 'Ordenar por', 'm') + f'<path d="M1096 {top + 24} l5 5 l5 -5" class="glm"/>'
    xs = (400, 654, 908); rows = 1 if filtered else 2
    for r in range(rows):
        for c in range(3): b += PCARD(xs[c], top + 76 + 350 * r, 232)
    fy = top + 840
    return b + FOOT(fy), fy + 170
