#!/usr/bin/env python3
import os
import sys
import argparse
from getpass import getpass

# Detectar módulo de configuración automáticamente
def detectar_settings():
    try:
        with open('manage.py', 'r') as f:
            content = f.read()
            import re
            match = re.search(r"DJANGO_SETTINGS_MODULE['\"],\s*['\"]([^'\"]+)['\"]", content)
            if match:
                return match.group(1)
    except:
        pass
    # Buscar carpetas con settings.py
    import glob
    for path in glob.glob('*/settings.py'):
        folder = path.split('/')[0]
        return f"{folder}.settings"
    return 'linguakit.settings'

settings_module = detectar_settings()
print(f"🔍 Usando configuración: {settings_module}")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

import django
django.setup()

from django.contrib.auth.models import User

def crear_usuario(tipo, username, password, email, first_name='', last_name=''):
    """
    Crea un usuario con el rol especificado.
    Tipos: 'admin', 'teacher', 'student'
    """
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe")
        return False

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        return False

    # Asignar permisos según el tipo
    if tipo == 'admin':
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"✅ Administrador creado: {username}")
    elif tipo == 'teacher':
        user.is_staff = True
        user.save()
        print(f"✅ Profesor creado: {username}")
    elif tipo == 'student':
        print(f"✅ Estudiante creado: {username}")
    else:
        user.delete()
        print(f"❌ Tipo de usuario inválido: {tipo}")
        return False

    print(f"   Email: {email}")
    print(f"   Nombre completo: {user.get_full_name() or 'No especificado'}")
    print("\n📌 Recuerda: Si necesitas asignar un perfil con rol específico, ve a /admin/ y edita el perfil del usuario en la sección correspondiente.")
    return True

def main():
    parser = argparse.ArgumentParser(description='Crear usuarios con roles en Linguakit-Academy')
    parser.add_argument('--type', choices=['admin', 'teacher', 'student'], required=True,
                        help='Tipo de usuario: admin, teacher, student')
    parser.add_argument('--username', required=True, help='Nombre de usuario')
    parser.add_argument('--password', required=True, help='Contraseña')
    parser.add_argument('--email', required=True, help='Correo electrónico')
    parser.add_argument('--first_name', default='', help='Nombre')
    parser.add_argument('--last_name', default='', help='Apellido')
    parser.add_argument('--interactive', action='store_true', help='Modo interactivo')

    args = parser.parse_args()
    crear_usuario(args.type, args.username, args.password, args.email,
                  args.first_name, args.last_name)

if __name__ == '__main__':
    main()
