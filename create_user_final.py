#!/usr/bin/env python3
"""
Script para crear usuarios en Linguakit-Academy
Adaptado a modelo de usuario personalizado
"""

import os
import sys
import argparse
from getpass import getpass

# Detectar configuración automáticamente
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

from django.contrib.auth import get_user_model
User = get_user_model()

# Intentar importar modelos de roles (si existen)
try:
    from apps.usuarios.models import Usuario, Rol  # si existe
    HAS_ROLES = True
except ImportError:
    HAS_ROLES = False

try:
    from apps.core.models import PerfilUsuario
    HAS_PERFIL = True
except ImportError:
    HAS_PERFIL = False

def crear_usuario(tipo, username, password, email, first_name='', last_name=''):
    """Crea un usuario con el rol especificado"""
    
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe")
        return False

    # Datos base
    user_data = {
        'username': username,
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
    }

    # Si el modelo tiene campos extra, adaptar
    try:
        # Intentar crear con todos los campos
        user = User.objects.create_user(**user_data)
    except TypeError as e:
        # Si falla, crear solo con los campos básicos
        print(f"⚠️ Creando solo con campos básicos: {e}")
        user = User.objects.create_user(username=username, email=email, password=password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()

    # Asignar roles según el tipo
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
        print(f"❌ Tipo inválido: {tipo}")
        return False

    # Si existe PerfilUsuario, crearlo
    if HAS_PERFIL:
        try:
            from apps.core.models import PerfilUsuario
            PerfilUsuario.objects.create(
                usuario=user,
                rol=tipo.upper(),
                identificacion=f"{tipo[:4].upper()}-{user.id:06d}"
            )
            print(f"   Perfil creado en core")
        except Exception as e:
            print(f"⚠️ No se pudo crear PerfilUsuario: {e}")

    # Si existe el modelo Usuario con roles, asignar
    if HAS_ROLES:
        try:
            from apps.usuarios.models import Usuario
            # Asignar rol según el tipo
            rol_map = {
                'admin': 'ADMIN',
                'teacher': 'PROFESOR',
                'student': 'ESTUDIANTE'
            }
            # Si el modelo tiene campo 'rol'
            if hasattr(user, 'rol'):
                user.rol = rol_map.get(tipo, 'ESTUDIANTE')
                user.save()
                print(f"   Rol asignado: {user.rol}")
        except Exception as e:
            print(f"⚠️ No se pudo asignar rol en usuarios: {e}")

    # Mostrar resumen
    print("\n📋 Resumen:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Tipo: {tipo}")
    print(f"   Superusuario: {user.is_superuser}")
    print(f"   Staff: {user.is_staff}")

    return True

def modo_interactivo():
    print("\n" + "=" * 50)
    print("👤 CREAR USUARIO - MODO INTERACTIVO")
    print("=" * 50)
    
    print("\nTipos:")
    print("  1. Administrador")
    print("  2. Profesor")
    print("  3. Estudiante")
    opcion = input("Selecciona (1-3): ").strip()
    
    tipos = {'1': 'admin', '2': 'teacher', '3': 'student'}
    tipo = tipos.get(opcion)
    if not tipo:
        print("❌ Opción inválida")
        return
    
    username = input("Usuario: ").strip()
    if not username:
        print("❌ Usuario requerido")
        return
    
    password = getpass("Contraseña: ")
    password2 = getpass("Confirmar: ")
    if password != password2:
        print("❌ No coinciden")
        return
    
    email = input("Email: ").strip()
    first_name = input("Nombre: ").strip()
    last_name = input("Apellido: ").strip()
    
    crear_usuario(tipo, username, password, email, first_name, last_name)

def main():
    parser = argparse.ArgumentParser(description='Crear usuarios en Linguakit-Academy')
    parser.add_argument('--type', choices=['admin', 'teacher', 'student'],
                        help='Tipo de usuario')
    parser.add_argument('--username', help='Nombre de usuario')
    parser.add_argument('--password', help='Contraseña')
    parser.add_argument('--email', help='Correo electrónico')
    parser.add_argument('--first_name', default='', help='Nombre')
    parser.add_argument('--last_name', default='', help='Apellido')
    parser.add_argument('--interactive', action='store_true', help='Modo interactivo')
    
    args = parser.parse_args()
    
    if args.interactive:
        modo_interactivo()
        return
    
    if not args.type or not args.username or not args.password or not args.email:
        print("❌ Faltan argumentos")
        print("   Uso: python create_user_final.py --type admin --username user --password pass --email e@x.com")
        print("   Interactivo: python create_user_final.py --interactive")
        sys.exit(1)
    
    crear_usuario(args.type, args.username, args.password, args.email,
                  args.first_name, args.last_name)

if __name__ == '__main__':
    main()
