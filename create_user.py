#!/usr/bin/env python3
import os
import sys
import argparse
from getpass import getpass

# Detectar automáticamente el módulo de configuración
def detectar_settings():
    # 1. Buscar en manage.py
    try:
        with open('manage.py', 'r') as f:
            content = f.read()
            import re
            # Buscar DJANGO_SETTINGS_MODULE
            match = re.search(r"os\.environ\.setdefault\(['\"]DJANGO_SETTINGS_MODULE['\"],\s*['\"]([^'\"]+)['\"]", content)
            if match:
                return match.group(1)
    except:
        pass
    
    # 2. Buscar carpetas que contengan settings.py
    import glob
    for path in glob.glob('*/settings.py'):
        # Obtener el nombre de la carpeta
        folder = path.split('/')[0]
        return f"{folder}.settings"
    
    # 3. Buscar carpetas que parezcan proyectos
    import os
    for item in os.listdir('.'):
        if os.path.isdir(item) and not item.startswith('.'):
            if os.path.exists(f"{item}/settings.py"):
                return f"{item}.settings"
    
    # 4. Por defecto
    return 'config.settings'

settings_module = detectar_settings()
print(f"🔍 Usando configuración: {settings_module}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
import django
django.setup()

from django.contrib.auth.models import User
from apps.core.models import PerfilUsuario

def crear_usuario(tipo, username, password, email, first_name='', last_name='', identificacion=None):
    # ... (el resto del código)
    pass

# ... (el resto del script)
