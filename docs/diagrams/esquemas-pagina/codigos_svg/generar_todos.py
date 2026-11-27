# -*- coding: utf-8 -*-
"""generar_todos.py - Ejecuta todos los scripts de pantalla de esta carpeta."""
import os, subprocess, sys
carpeta = os.path.dirname(os.path.abspath(__file__))
extra = sys.argv[1:]
for nombre in sorted(os.listdir(carpeta)):
    if nombre.endswith('.py') and nombre not in ('comun.py', 'generar_todos.py'):
        subprocess.run([sys.executable, os.path.join(carpeta, nombre)] + extra, check=True)
