#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador automático de Rhetorica+ (Django)
=============================================
Este script instala y configura completamente el proyecto Django
con todos los módulos: retórica, etimología, periodismo, gramática,
fonología, semiótica, lingüística, sintaxis, antropolingüística,
literatura, semántica, narrativa, párrafos, oraciones, ortografía,
textolingüística, pragmática, etnolingüística, puntuación.
"""

import os
import sys
import subprocess
import json
import shutil
import stat
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

PROJECT_NAME = "rhetorica_plus"
PROJECT_DIR = Path.cwd() / PROJECT_NAME
VENV_DIR = PROJECT_DIR / "venv"
DATA_DIR = PROJECT_DIR / "data"
TEMPLATES_DIR = PROJECT_DIR / "core" / "templates" / "core"
STATIC_DIR = PROJECT_DIR / "static"
MEDIA_DIR = PROJECT_DIR / "media"

# Lista de secciones con sus configuraciones
SECTIONS = [
    {"name": "retorica", "title": "Retórica", "icon": "fa-comment-dots", "json_file": "retorica.json"},
    {"name": "etimologia", "title": "Etimología", "icon": "fa-language", "json_file": "etimologia.json"},
    {"name": "periodismo", "title": "Periodismo", "icon": "fa-newspaper", "json_file": "periodismo.json"},
    {"name": "gramatica", "title": "Gramática", "icon": "fa-spell-check", "json_file": "gramatica.json"},
    {"name": "fonologia", "title": "Fonología", "icon": "fa-microphone-alt", "json_file": "fonologia.json"},
    {"name": "semiotica", "title": "Semiótica", "icon": "fa-signs-post", "json_file": "semiotica.json"},
    {"name": "linguistica", "title": "Lingüística", "icon": "fa-language", "json_file": "linguistica.json"},
    {"name": "sintaxis", "title": "Sintaxis", "icon": "fa-code-branch", "json_file": "sintaxis.json"},
    {"name": "antropolinguistica", "title": "Antropolingüística", "icon": "fa-globe-americas", "json_file": "antropolinguistica.json"},
    {"name": "literatura", "title": "Literatura", "icon": "fa-book-open", "json_file": "literatura.json"},
    {"name": "semantica", "title": "Semántica", "icon": "fa-brain", "json_file": "semantica.json"},
    {"name": "narrativa", "title": "Narrativa", "icon": "fa-book", "json_file": "narrativa.json"},
    {"name": "parrafos", "title": "Párrafos", "icon": "fa-paragraph", "json_file": "parrafos.json"},
    {"name": "oraciones", "title": "Oraciones", "icon": "fa-sitemap", "json_file": "oraciones.json"},
    {"name": "ortografia", "title": "Ortografía", "icon": "fa-spell-check", "json_file": "ortografia.json"},
    {"name": "textolinguistica", "title": "Textolingüística", "icon": "fa-file-alt", "json_file": "textolinguistica.json"},
    {"name": "pragmatica", "title": "Pragmática", "icon": "fa-comment", "json_file": "pragmatica.json"},
    {"name": "etnolinguistica", "title": "Etnolingüística", "icon": "fa-globe", "json_file": "etnolinguistica.json"},
    {"name": "puntuacion", "title": "Puntuación", "icon": "fa-code", "json_file": "puntuacion.json"},
]

# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(text):
    """Imprime un paso del proceso."""
    print(f"\n▶ {text}")


def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"  ✅ {text}")


def print_warning(text):
    """Imprime una advertencia."""
    print(f"  ⚠️ {text}")


def print_error(text):
    """Imprime un error."""
    print(f"  ❌ {text}")


def run_command(cmd, cwd=None, capture_output=False):
    """Ejecuta un comando del sistema."""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode, "", ""
    except Exception as e:
        return -1, "", str(e)


def ensure_dir(path):
    """Crea un directorio si no existe."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def delete_dir(path):
    """Elimina un directorio si existe."""
    if Path(path).exists():
        shutil.rmtree(path)


def create_file(path, content):
    """Crea un archivo con contenido."""
    ensure_dir(Path(path).parent)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


# ============================================================
# GENERACIÓN DE ARCHIVOS
# ============================================================

def create_settings_py():
    """Genera el archivo settings.py"""
    content = '''"""
Django settings for rhetorica_plus project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@#$retorica_viva_2024_secret_key_change_in_production$%&'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rhetorica_plus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rhetorica_plus.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración personalizada
AUTH_USER_MODEL = 'core.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'index'

# CSRF para desarrollo en Codespaces
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://localhost:8000',
    'http://127.0.0.1:8000',
    'https://127.0.0.1:8000',
]
if os.environ.get('CODESPACE_NAME'):
    CSRF_TRUSTED_ORIGINS.append(f'https://{os.environ["CODESPACE_NAME"]}-8000.preview.app.github.dev')

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
'''
    return content


def create_urls_py():
    """Genera el archivo urls.py del proyecto."""
    content = '''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
'''
    return content


def create_wsgi_py():
    """Genera el archivo wsgi.py."""
    content = '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rhetorica_plus.settings')
application = get_wsgi_application()
'''
    return content


def create_asgi_py():
    """Genera el archivo asgi.py."""
    content = '''import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rhetorica_plus.settings')
application = get_asgi_application()
'''
    return content


def create_models_py():
    """Genera el archivo models.py de la app core."""
    content = '''from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    points = models.IntegerField(default=0)
    nivel = models.CharField(max_length=20, default='Aprendiz')
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.points < 100:
            self.nivel = 'Aprendiz'
        elif self.points < 300:
            self.nivel = 'Conocedor'
        elif self.points < 600:
            self.nivel = 'Experto'
        else:
            self.nivel = 'Maestro Retórico'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Respuesta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas')
    tipo_ejercicio = models.CharField(max_length=50)
    item_id = models.IntegerField()
    respuesta_usuario = models.TextField()
    es_correcta = models.BooleanField(default=False)
    puntuacion = models.IntegerField(default=0)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.tipo_ejercicio} - {self.fecha}"

class ProgresoCategoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso')
    categoria = models.CharField(max_length=100)
    aciertos = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)

    @property
    def porcentaje(self):
        if self.intentos == 0:
            return 0
        return round((self.aciertos / self.intentos) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.categoria}: {self.porcentaje}%"
'''
    return content


def create_admin_py():
    """Genera el archivo admin.py."""
    content = '''from django.contrib import admin
from .models import User, Respuesta, ProgresoCategoria

admin.site.register(User)
admin.site.register(Respuesta)
admin.site.register(ProgresoCategoria)
'''
    return content


def create_apps_py():
    """Genera el archivo apps.py."""
    content = '''from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
'''
    return content


def create_forms_py():
    """Genera el archivo forms.py."""
    content = '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
'''
    return content


def create_decorators_py():
    """Genera el archivo decorators.py."""
    content = '''from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, 'Acceso denegado. Se requieren privilegios de administrador.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
'''
    return content


def create_views_py():
    """Genera el archivo views.py con todas las vistas para las secciones."""
    # Creamos la lista de imports y la carga de datos dinámicamente
    sections_import = ""
    data_vars = {}
    
    for i, section in enumerate(SECTIONS):
        var_name = f"{section['name'].upper()}_DATA"
        data_vars[section['name']] = var_name
    
    # Carga de datos
    load_data = ""
    for section in SECTIONS:
        var_name = data_vars[section['name']]
        load_data += f'''
with open(os.path.join(BASE_DIR, "data", "{section['json_file']}"), "r", encoding="utf-8") as f:
    {var_name} = json.load(f)'''
    
    # Vistas
    views_func = ""
    for section in SECTIONS:
        var_name = data_vars[section['name']]
        views_func += f'''
@login_required
def {section['name']}(request):
    return render(request, "core/{section['name']}.html", {{"tecnicas": {var_name}}})
'''
    
    content = f'''import json, random, os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import User, Respuesta, ProgresoCategoria
from .forms import RegistroForm
from .decorators import admin_required

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
{load_data}

# ============================================================
# VISTAS PÚBLICAS
# ============================================================

def index(request):
    return render(request, 'core/index.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {{'form': form}})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    total = Respuesta.objects.filter(user=request.user).count()
    correctas = Respuesta.objects.filter(user=request.user, es_correcta=True).count()
    porcentaje = round((correctas / total) * 100) if total else 0
    progreso = ProgresoCategoria.objects.filter(user=request.user)
    ultimas = Respuesta.objects.filter(user=request.user).order_by('-fecha')[:10]
    recomendaciones = []
    if total < 20:
        recomendaciones.append("Completa más ejercicios para ganar puntos")
    return render(request, 'core/dashboard.html', {{
        'usuario': request.user, 'total': total, 'correctas': correctas,
        'porcentaje': porcentaje, 'progreso': progreso, 'ultimas': ultimas,
        'recomendaciones': recomendaciones
    }})

# ============================================================
# SECCIONES DE ESTUDIO
# ============================================================
{views_func}

# ============================================================
# EXÁMENES Y API
# ============================================================

@login_required
def examen_form(request):
    if request.method == 'POST':
        tema = request.POST.get('tema')
        num = int(request.POST.get('num_preguntas', 10))
        return render(request, 'core/examen.html', {{'tema': tema, 'num': num}})
    return render(request, 'core/examen_form.html')

@csrf_exempt
@login_required
def api_generar_preguntas(request):
    data = json.loads(request.body)
    tema = data.get('tema')
    num = data.get('num', 10)
    fuente = globals().get(f"{{tema.upper()}}_DATA", [])
    if not fuente:
        return JsonResponse([], safe=False)
    items = random.sample(fuente, min(num, len(fuente)))
    preguntas = []
    for item in items:
        if tema == 'retorica':
            respuesta = item['name']
            otros = [f for f in globals().get('RETORICA_DATA', []) if f['name'] != respuesta]
            distractores = [f['name'] for f in random.sample(otros, min(3, len(otros)))]
            pregunta = f"¿Qué figura es? {{item['teoria'][:80]}}..."
            categoria = item.get('category', 'Retórica')
        else:
            respuesta = item['name']
            otros = [f for f in fuente if f.get('name') != respuesta]
            distractores = [f['name'] for f in random.sample(otros, min(3, len(otros)))]
            pregunta = f"¿Qué concepto es? {{item['teoria'][:80]}}..."
            categoria = item.get('category', tema.capitalize())
        opciones = [respuesta] + distractores[:3]
        random.shuffle(opciones)
        preguntas.append({{
            'id': item['id'],
            'pregunta': pregunta,
            'respuesta_correcta': respuesta,
            'opciones': opciones,
            'categoria': categoria
        }})
    return JsonResponse(preguntas, safe=False)

@csrf_exempt
@login_required
def api_guardar_respuesta(request):
    data = json.loads(request.body)
    puntos = 10 if data.get('es_correcta') else 0
    Respuesta.objects.create(
        user=request.user,
        tipo_ejercicio=data.get('tipo', 'examen'),
        item_id=data.get('item_id'),
        respuesta_usuario=data.get('respuesta_usuario'),
        es_correcta=data.get('es_correcta'),
        puntuacion=puntos
    )
    request.user.points += puntos
    request.user.save()
    cat = data.get('categoria', 'General')
    prog, _ = ProgresoCategoria.objects.get_or_create(user=request.user, categoria=cat)
    prog.intentos += 1
    if data.get('es_correcta'):
        prog.aciertos += 1
    prog.save()
    return JsonResponse({{'success': True, 'puntos': puntos}})

# ============================================================
# PANEL DE ADMINISTRACIÓN
# ============================================================

@login_required
@admin_required
def admin_panel(request):
    usuarios = User.objects.all()
    total_resp = Respuesta.objects.count()
    total_pts = Respuesta.objects.aggregate(total=models.Sum('puntuacion'))['total'] or 0
    stats = []
    for u in usuarios:
        resp = Respuesta.objects.filter(user=u).count()
        corr = Respuesta.objects.filter(user=u, es_correcta=True).count()
        stats.append({{
            'id': u.id, 'username': u.username, 'email': u.email,
            'respuestas': resp, 'correctas': corr, 'puntos': u.points,
            'nivel': u.nivel, 'is_admin': u.is_admin,
            'fecha_registro': u.date_joined
        }})
    return render(request, 'core/admin_panel.html', {{
        'usuarios': stats, 'total_usuarios': len(usuarios),
        'total_respuestas': total_resp, 'total_puntos': total_pts
    }})

@login_required
@admin_required
def admin_nuevo_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_admin = request.POST.get('is_admin') == 'on'
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ya existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email ya registrado')
        else:
            User.objects.create_user(username=username, email=email, password=password, is_admin=is_admin)
            messages.success(request, f'Usuario {{username}} creado')
            return redirect('admin_panel')
    return render(request, 'core/admin_nuevo_usuario.html')

@login_required
@admin_required
def toggle_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'No puedes cambiarte a ti mismo')
    else:
        user.is_admin = not user.is_admin
        user.save()
        messages.success(request, f'Privilegios actualizados para {{user.username}}')
    return redirect('admin_panel')

@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'No puedes eliminarte')
    else:
        user.delete()
        messages.success(request, f'Usuario {{user.username}} eliminado')
    return redirect('admin_panel')

# ============================================================
# PROYECTO PEDAGÓGICO
# ============================================================

@login_required
def proyecto(request):
    return render(request, 'core/proyecto.html')
'''
    return content


def create_core_urls_py():
    """Genera el archivo urls.py de la app core."""
    sections_urls = ""
    for section in SECTIONS:
        sections_urls += f"    path('{section['name']}/', views.{section['name']}, name='{section['name']}'),\n"
    
    content = f'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
{sections_urls}    path('examen/', views.examen_form, name='examen_form'),
    path('api/generar_preguntas/', views.api_generar_preguntas, name='api_generar'),
    path('api/guardar_respuesta/', views.api_guardar_respuesta, name='api_guardar'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/nuevo/', views.admin_nuevo_usuario, name='admin_nuevo_usuario'),
    path('admin-panel/toggle/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('admin-panel/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('proyecto/', views.proyecto, name='proyecto'),
]
'''
    return content


def create_base_html():
    """Genera el template base.html."""
    content = '''{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rhetorica+</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body { background: #f5f3ef; font-family: 'Segoe UI', system-ui, sans-serif; }
        .navbar-brand { font-weight: 700; font-size: 1.5rem; }
        .footer { background: #1e2a3a; color: #cddde9; margin-top: 3rem; padding: 1.5rem 0; text-align: center; }
        .card-flash { transition: transform 0.2s, box-shadow 0.2s; border-radius: 1.2rem; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .card-flash:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .btn-sound { background: #2c3e50; color: white; border-radius: 40px; padding: 0.25rem 0.9rem; font-size: 0.75rem; }
        .btn-sound:hover { background: #d4af37; color: #1e2a3a; }
        .original-script { font-family: 'Times New Roman', serif; font-size: 1.1rem; background: #f0ece4; padding: 0.2rem 0.6rem; border-radius: 20px; }
        .float-voice-btn { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; border-radius: 50%; background: #2c3e50; color: white; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.2); cursor: pointer; z-index: 1000; transition: 0.3s; }
        .float-voice-btn:hover { background: #d4af37; color: #1e2a3a; transform: scale(1.1); }
        .voice-controls { position: fixed; bottom: 100px; right: 30px; background: white; border-radius: 15px; padding: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 999; display: none; }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg bg-dark navbar-dark sticky-top">
    <div class="container">
        <a class="navbar-brand" href="{% url 'index' %}"><i class="fas fa-scroll me-2"></i>Rhetorica+</a>
        <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'retorica' %}">Retórica</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'etimologia' %}">Etimología</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'examen_form' %}">Examen</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a></li>
                    {% if user.is_admin %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'admin_panel' %}">Admin</a></li>
                    {% endif %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'proyecto' %}">Proyecto</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'logout' %}">Salir</a></li>
                {% else %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Login</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'registro' %}">Registro</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'proyecto' %}">Proyecto</a></li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
<main class="container my-4">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">{{ message }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
        {% endfor %}
    {% endif %}
    {% block content %}{% endblock %}
</main>
<footer class="footer"><div class="container"><small><i class="fas fa-microphone-alt"></i> Lector de voz integrado · Todas las disciplinas lingüísticas y literarias</small></div></footer>
<button class="float-voice-btn" onclick="toggleVoiceControls()"><i class="fas fa-head-side-vr fa-2x"></i></button>
<div class="voice-controls" id="voiceControls">
    <div class="d-flex flex-column gap-2">
        <button class="btn btn-sm btn-primary" onclick="readPageContent()"><i class="fas fa-play"></i> Leer página</button>
        <button class="btn btn-sm btn-secondary" onclick="stopSpeech()"><i class="fas fa-stop"></i> Detener</button>
        <select id="voiceSelect" class="form-select form-select-sm" onchange="setVoice()"></select>
        <input type="range" id="rateControl" min="0.5" max="2" step="0.1" value="0.9" onchange="setRate()">
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
<script>
    let currentUtterance = null, availableVoices = [];
    function toggleVoiceControls() { let c = document.getElementById('voiceControls'); c.style.display = c.style.display === 'none' ? 'block' : 'none'; if (!availableVoices.length) loadVoices(); }
    function loadVoices() { availableVoices = window.speechSynthesis.getVoices(); let sel = document.getElementById('voiceSelect'); let es = availableVoices.filter(v=>v.lang.startsWith('es')); let list = es.length ? es : availableVoices; sel.innerHTML = '<option value="">Voz por defecto</option>' + list.map(v=>`<option value="$${v.name}">$${v.name} ($${v.lang})</option>`).join(''); }
    if(window.speechSynthesis) window.speechSynthesis.onvoiceschanged = loadVoices;
    function setVoice() { if(!currentUtterance) return; let name = document.getElementById('voiceSelect').value; if(name) currentUtterance.voice = availableVoices.find(v=>v.name===name); }
    function setRate() { if(currentUtterance) currentUtterance.rate = parseFloat(document.getElementById('rateControl').value); }
    function speakText(t) { if(!window.speechSynthesis) return; if(currentUtterance) window.speechSynthesis.cancel(); currentUtterance = new SpeechSynthesisUtterance(t); currentUtterance.lang = 'es-ES'; currentUtterance.rate = parseFloat(document.getElementById('rateControl').value); let name = document.getElementById('voiceSelect').value; if(name) currentUtterance.voice = availableVoices.find(v=>v.name===name); window.speechSynthesis.speak(currentUtterance); }
    function stopSpeech() { if(window.speechSynthesis) window.speechSynthesis.cancel(); currentUtterance=null; }
    function readPageContent() { let txt = ''; document.querySelectorAll('main h1, main h2, main h3, main p, main li, .card-text, .alert').forEach(el=>{ if(el.innerText) txt+=el.innerText+'. '; }); if(txt) speakText(txt.substring(0,3000)); else speakText('No hay contenido para leer'); }
</script>
{% block scripts %}{% endblock %}
</body>
</html>
'''
    return content


def create_index_html():
    """Genera el template index.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="text-center py-5">
    <h1 class="display-4">Bienvenido a Rhetorica+</h1>
    <p class="lead">Plataforma interactiva para el aprendizaje de lingüística, literatura y retórica</p>
    {% if not user.is_authenticated %}
        <a href="{% url 'login' %}" class="btn btn-primary btn-lg">Iniciar sesión</a>
        <a href="{% url 'registro' %}" class="btn btn-success btn-lg">Registrarse</a>
    {% else %}
        <a href="{% url 'retorica' %}" class="btn btn-primary btn-lg">Comenzar a practicar</a>
    {% endif %}
</div>
<div class="row mt-5">
    <div class="col-md-4"><div class="card text-center p-3"><i class="fas fa-comment-dots fa-3x text-success"></i><h3>Retórica</h3><p>100 técnicas retóricas con ejercicios</p></div></div>
    <div class="col-md-4"><div class="card text-center p-3"><i class="fas fa-language fa-3x text-warning"></i><h3>Etimología</h3><p>100 raíces grecolatinas</p></div></div>
    <div class="col-md-4"><div class="card text-center p-3"><i class="fas fa-chart-line fa-3x text-info"></i><h3>Dashboard</h3><p>Seguimiento de progreso</p></div></div>
</div>
{% endblock %}
'''
    return content


def create_login_html():
    """Genera el template login.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white"><h3>Iniciar sesión</h3></div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3"><label>Usuario</label><input type="text" name="username" class="form-control" required></div>
                    <div class="mb-3"><label>Contraseña</label><input type="password" name="password" class="form-control" required></div>
                    <button type="submit" class="btn btn-primary w-100">Ingresar</button>
                </form>
                <hr><p class="text-center">¿No tienes cuenta? <a href="{% url 'registro' %}">Regístrate</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    return content


def create_registro_html():
    """Genera el template registro.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card shadow">
            <div class="card-header bg-success text-white"><h3>Registro</h3></div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.non_field_errors }}
                    <div class="mb-3"><label>Usuario</label>{{ form.username }}</div>
                    <div class="mb-3"><label>Email</label>{{ form.email }}</div>
                    <div class="mb-3"><label>Contraseña</label>{{ form.password1 }}</div>
                    <div class="mb-3"><label>Confirmar contraseña</label>{{ form.password2 }}</div>
                    <button type="submit" class="btn btn-success w-100">Registrarse</button>
                </form>
                <hr><p class="text-center">¿Ya tienes cuenta? <a href="{% url 'login' %}">Inicia sesión</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    return content


def create_dashboard_html():
    """Genera el template dashboard.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<h2><i class="fas fa-tachometer-alt"></i> Mi Dashboard</h2>
<div class="row g-4 mb-4">
    <div class="col-md-3"><div class="card bg-primary text-white text-center"><div class="card-body"><i class="fas fa-star fa-2x"></i><h3>{{ usuario.points }}</h3><p>Puntos</p></div></div></div>
    <div class="col-md-3"><div class="card bg-success text-white text-center"><div class="card-body"><i class="fas fa-check-circle fa-2x"></i><h3>{{ correctas }}/{{ total }}</h3><p>Aciertos</p></div></div></div>
    <div class="col-md-3"><div class="card bg-info text-white text-center"><div class="card-body"><i class="fas fa-chart-line fa-2x"></i><h3>{{ porcentaje }}%</h3><p>Rendimiento</p></div></div></div>
    <div class="col-md-3"><div class="card bg-warning text-dark text-center"><div class="card-body"><i class="fas fa-medal fa-2x"></i><h3>{{ usuario.nivel }}</h3><p>Nivel</p></div></div></div>
</div>
<div class="row"><div class="col-md-6"><div class="card"><div class="card-header">Progreso por categorías</div><div class="card-body">{% for p in progreso %}<b>{{ p.categoria }}</b>: {{ p.porcentaje }}% ({{ p.aciertos }}/{{ p.intentos }})<div class="progress mb-2"><div class="progress-bar bg-success" style="width:{{ p.porcentaje }}%"></div></div>{% empty %}Sin datos aún{% endfor %}</div></div></div>
<div class="col-md-6"><div class="card"><div class="card-header">Recomendaciones</div><div class="card-body">{% for rec in recomendaciones %}<li>{{ rec }}</li>{% empty %}¡Sigue así!{% endfor %}</div></div></div></div>
<div class="mt-4 text-center"><a href="{% url 'retorica' %}" class="btn btn-success">Retórica</a> <a href="{% url 'etimologia' %}" class="btn btn-warning">Etimología</a> <a href="{% url 'examen_form' %}" class="btn btn-primary">Examen</a></div>
{% endblock %}
'''
    return content


def create_section_template(section):
    """Genera el template para una sección específica."""
    content = f'''{{% extends "core/base.html" %}}
{{% block content %}}
<h2><i class="fas {section['icon']}"></i> {{section['title']}}</h2>
<div class="alert alert-info"><i class="fas fa-graduation-cap"></i> 100 técnicas de {{section['title'].lower()}}.</div>
<div class="row g-4">
    {{% for t in tecnicas %}}
    <div class="col-md-6 col-lg-4">
        <div class="card card-flash h-100">
            <div class="card-header bg-transparent border-0 pt-3">
                <div class="d-flex justify-content-between">
                    <div><h5 class="fw-bold">{{{{ t.name }}}}</h5><span class="badge bg-secondary">{{{{ t.category }}}}</span></div>
                    <button class="btn btn-sound btn-sm" onclick="speakText('{{{{ t.name }}}}. {{{{ t.teoria }}}} Ejemplo: {{{{ t.ejemplo }}}}')"><i class="fas fa-volume-up"></i> Leer</button>
                </div>
            </div>
            <div class="card-body">
                <div class="bg-light p-2 rounded"><strong>Teoría:</strong> {{{{ t.teoria }}}}</div>
                <div class="bg-warning bg-opacity-10 p-2 rounded mt-2"><strong>Ejemplo:</strong> “{{{{ t.ejemplo }}}}”</div>
                <div class="mt-3">
                    <label class="fw-semibold">✍️ {{{{ t.ejercicio }}}}</label>
                    <textarea id="ans-{{{{ t.id }}}}" class="form-control mt-2" rows="2" placeholder="Escribe tu respuesta..."></textarea>
                    <button class="btn btn-outline-success btn-sm mt-2" onclick="guardarRespuesta({{{{ t.id }}}}, '{{{{ t.suggestedAnswer|escapejs }}}}', '{section['name']}')">Verificar y guardar</button>
                    <div id="fb-{{{{ t.id }}}}" class="small mt-2"></div>
                </div>
            </div>
        </div>
    </div>
    {{% endfor %}}
</div>
<script>
function guardarRespuesta(id, sugerencia, tipo) {{
    let userAns = document.getElementById('ans-'+id).value;
    let fb = document.getElementById('fb-'+id);
    let correcta = userAns.length > 10;
    fetch('/api/guardar_respuesta/', {{
        method: 'POST',
        headers: {{'Content-Type':'application/json', 'X-CSRFToken':'{{ csrf_token }}'}},
        body: JSON.stringify({{tipo: tipo, item_id: id, es_correcta: correcta, respuesta_usuario: userAns, categoria: '{section['title']}'}})
    }}).then(r=>r.json()).then(data=>{{
        let msg = correcta ? '<span class="text-success">✓ Correcto (+10 pts)</span>' : '<span class="text-info">Respuesta guardada</span>';
        fb.innerHTML = msg + '<br><strong>Sugerencia:</strong> ' + sugerencia;
    }});
}}
</script>
{{% endblock %}}
'''
    return content


def create_examen_form_html():
    """Genera el template examen_form.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-primary text-white"><h4>Configurar examen</h4></div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3"><label>Temática</label><select name="tema" class="form-select"><option value="retorica">Retórica</option><option value="etimologia">Etimología</option></select></div>
                    <div class="mb-3"><label>Número de preguntas</label><input type="number" name="num_preguntas" class="form-control" value="10" min="5" max="50"></div>
                    <button type="submit" class="btn btn-success w-100">Generar examen</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    return content


def create_examen_html():
    """Genera el template examen.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<h2><i class="fas fa-pen-alt"></i> Examen de {{ tema|capfirst }} <span class="badge bg-primary">{{ num }} preguntas</span></h2>
<div id="examContainer"></div>
<div class="mt-3 d-flex gap-3"><button id="checkAll" class="btn btn-primary">Revisar todas</button> <button id="resetBtn" class="btn btn-secondary">Limpiar</button> <a href="{% url 'examen_form' %}" class="btn btn-outline-success">Nuevo examen</a></div>
<script>
const tema = "{{ tema }}", num = {{ num }};
let preguntas = [];
fetch('/api/generar_preguntas/', {
    method: 'POST', headers: {'Content-Type':'application/json', 'X-CSRFToken':'{{ csrf_token }}'},
    body: JSON.stringify({tema:tema, num:num})
}).then(r=>r.json()).then(data=>{ preguntas=data; render(); });
function render() {
    const container = document.getElementById('examContainer');
    container.innerHTML = '';
    preguntas.forEach((q,idx)=>{
        const card = document.createElement('div');
        card.className = 'card mb-3';
        card.innerHTML = `<div class="card-body"><h5>${idx+1}. ${q.pregunta}</h5>${q.opciones.map((opt,i)=>`<div class="form-check"><input class="form-check-input" type="radio" name="q${idx}" value="${opt}" id="q${idx}_${i}"><label for="q${idx}_${i}">${opt}</label></div>`).join('')}<button class="btn btn-sm btn-outline-primary mt-2" onclick="check(${idx})">Comprobar</button><div id="fb${idx}" class="small mt-2"></div></div>`;
        container.appendChild(card);
    });
}
function check(idx) {
    const selected = document.querySelector(`input[name="q${idx}"]:checked`);
    const fb = document.getElementById(`fb${idx}`);
    if(!selected){ fb.innerHTML='<span class="text-warning">Selecciona una opción</span>'; return; }
    const correct = (selected.value === preguntas[idx].respuesta_correcta);
    fb.innerHTML = correct ? `<span class="text-success">✓ Correcto</span>` : `<span class="text-danger">✗ Incorrecto. Respuesta: ${preguntas[idx].respuesta_correcta}</span>`;
    fetch('/api/guardar_respuesta/', {
        method:'POST', headers:{'Content-Type':'application/json', 'X-CSRFToken':'{{ csrf_token }}'},
        body: JSON.stringify({tipo:'examen', item_id:preguntas[idx].id, es_correcta:correct, respuesta_usuario:selected.value, categoria:preguntas[idx].categoria})
    });
}
document.getElementById('checkAll').onclick = () => { for(let i=0;i<preguntas.length;i++) check(i); };
document.getElementById('resetBtn').onclick = () => { document.querySelectorAll('input[type="radio"]').forEach(r=>r.checked=false); document.querySelectorAll('[id^="fb"]').forEach(f=>f.innerHTML=''); };
</script>
{% endblock %}
'''
    return content


def create_admin_panel_html():
    """Genera el template admin_panel.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="fas fa-shield-alt"></i> Panel de Administración</h2>
    <a href="{% url 'admin_nuevo_usuario' %}" class="btn btn-success"><i class="fas fa-user-plus"></i> Nuevo usuario</a>
</div>
<div class="row g-3 mb-4">
    <div class="col-md-4"><div class="card bg-primary text-white"><div class="card-body"><h3>{{ total_usuarios }}</h3><p>Usuarios</p></div></div></div>
    <div class="col-md-4"><div class="card bg-success text-white"><div class="card-body"><h3>{{ total_respuestas }}</h3><p>Ejercicios realizados</p></div></div></div>
    <div class="col-md-4"><div class="card bg-warning text-dark"><div class="card-body"><h3>{{ total_puntos }}</h3><p>Puntos totales</p></div></div></div>
</div>
<div class="card"><div class="card-body p-0"><div class="table-responsive"><table class="table table-hover mb-0">
    <thead class="table-light"><tr><th>ID</th><th>Usuario</th><th>Email</th><th>Respuestas</th><th>Puntos</th><th>Nivel</th><th>Admin</th><th>Acciones</th></tr></thead>
    <tbody>{% for u in usuarios %}<tr><td>{{ u.id }}</td><td>{{ u.username }}</td><td>{{ u.email }}</td><td>{{ u.respuestas }} ({{ u.correctas }} ✓)</td><td>{{ u.puntos }}</td><td>{{ u.nivel }}</td><td>{% if u.is_admin %}✅ Sí{% else %}❌ No{% endif %}</td>
    <td><form method="post" action="{% url 'toggle_admin' u.id %}" style="display:inline">{% csrf_token %}<button class="btn btn-sm btn-warning">🔁 Rol</button></form>
    <form method="post" action="{% url 'delete_user' u.id %}" style="display:inline" onsubmit="return confirm('¿Eliminar usuario?')">{% csrf_token %}<button class="btn btn-sm btn-danger">🗑️</button></form></td></td>{% endfor %}</tbody>
}班</div></div></div>
{% endblock %}
'''
    return content


def create_admin_nuevo_usuario_html():
    """Genera el template admin_nuevo_usuario.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<div class="row justify-content-center"><div class="col-md-6"><div class="card"><div class="card-header bg-primary text-white"><h4>Crear nuevo usuario</h4></div><div class="card-body"><form method="post">{% csrf_token %}<div class="mb-3"><label>Usuario</label><input type="text" name="username" class="form-control" required></div><div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div><div class="mb-3"><label>Contraseña</label><input type="password" name="password" class="form-control" required></div><div class="mb-3 form-check"><input type="checkbox" name="is_admin" class="form-check-input" id="is_admin"><label for="is_admin">Es administrador</label></div><button type="submit" class="btn btn-primary w-100">Crear usuario</button></form></div></div></div></div>
{% endblock %}
'''
    return content


def create_proyecto_html():
    """Genera el template proyecto.html."""
    content = '''{% extends "core/base.html" %}
{% block content %}
<h2><i class="fas fa-book-open"></i> Proyecto Pedagógico: Retórica Viva</h2>
<div class="card"><div class="card-body">
    <h3>Identificación</h3><p><strong>Título:</strong> Retórica Viva<br><strong>Duración:</strong> 12 semanas<br><strong>Nivel:</strong> 4º ESO - Universidad<br><strong>Tecnología:</strong> Django + Web Speech API</p>
    <h3>Justificación</h3><p>Aprendizaje activo, andamiaje, gamificación y Diseño Universal para el Aprendizaje.</p>
    <h3>Objetivos</h3><ul><li>Identificar y producir figuras retóricas</li><li>Reconocer raíces grecolatinas</li><li>Usar la plataforma autónomamente</li></ul>
    <h3>Evaluación</h3><p>Evaluación continua (70%): flashcards, exámenes, textos. Niveles: Aprendiz (0-99), Conocedor (100-299), Experto (300-599), Maestro Retórico (600+).</p>
    <h3>Presupuesto</h3><p>Servidor cloud: 30€, impresiones: 20€, diplomas: 15€, coordinación TIC: 200€ → <strong>Total 265€</strong>.</p>
    <blockquote>"La retórica es la facultad de descubrir lo que es adecuado para persuadir" — Aristóteles</blockquote>
</div></div>
{% endblock %}
'''
    return content


def create_manage_py():
    """Genera el archivo manage.py."""
    content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rhetorica_plus.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
    return content


def create_requirements_txt():
    """Genera el archivo requirements.txt."""
    content = '''Django>=4.2,<5.0
'''
    return content


# ============================================================
# FUNCIÓN PRINCIPAL DEL INSTALADOR
# ============================================================

def main():
    print_header("RHETORICA+ INSTALADOR AUTOMÁTICO")
    print("\nEste instalador creará y configurará el proyecto Django Rhetorica+")
    print("con todos los módulos lingüísticos y literarios (19 secciones).")
    
    # Verificar Python
    print_step("Verificando entorno Python...")
    if sys.version_info < (3, 8):
        print_error("Se requiere Python 3.8 o superior")
        sys.exit(1)
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    
    # Crear directorio del proyecto
    print_step(f"Creando directorio del proyecto: {PROJECT_DIR}")
    ensure_dir(PROJECT_DIR)
    
    # Crear entorno virtual
    print_step("Creando entorno virtual...")
    venv_python = VENV_DIR / "bin" / "python" if os.name != 'nt' else VENV_DIR / "Scripts" / "python.exe"
    
    if not VENV_DIR.exists():
        result, _, _ = run_command(f"python -m venv {VENV_DIR}")
        if result != 0:
            print_error("No se pudo crear el entorno virtual")
            sys.exit(1)
    print_success("Entorno virtual creado")
    
    # Activar entorno e instalar Django
    print_step("Instalando Django...")
    if os.name != 'nt':
        pip_cmd = f"{VENV_DIR}/bin/pip"
        python_cmd = f"{VENV_DIR}/bin/python"
    else:
        pip_cmd = f"{VENV_DIR}\\Scripts\\pip"
        python_cmd = f"{VENV_DIR}\\Scripts\\python"
    
    result, _, _ = run_command(f"{pip_cmd} install django")
    if result != 0:
        print_error("No se pudo instalar Django")
        sys.exit(1)
    print_success("Django instalado")
    
    # Crear proyecto y app
    os.chdir(PROJECT_DIR)
    
    print_step("Creando proyecto Django...")
    result, _, _ = run_command(f"{python_cmd} -m django startproject rhetorica_plus .")
    if result != 0:
        print_error("No se pudo crear el proyecto")
    
    print_step("Creando app core...")
    result, _, _ = run_command(f"{python_cmd} manage.py startapp core")
    
    # Crear carpetas
    ensure_dir(DATA_DIR)
    ensure_dir(TEMPLATES_DIR)
    ensure_dir(STATIC_DIR)
    ensure_dir(MEDIA_DIR)
    
    # Escribir archivos de configuración
    print_step("Generando archivos de configuración...")
    create_file(PROJECT_DIR / "rhetorica_plus" / "settings.py", create_settings_py())
    create_file(PROJECT_DIR / "rhetorica_plus" / "urls.py", create_urls_py())
    create_file(PROJECT_DIR / "rhetorica_plus" / "wsgi.py", create_wsgi_py())
    create_file(PROJECT_DIR / "rhetorica_plus" / "asgi.py", create_asgi_py())
    
    # Escribir archivos de la app core
    create_file(PROJECT_DIR / "core" / "models.py", create_models_py())
    create_file(PROJECT_DIR / "core" / "admin.py", create_admin_py())
    create_file(PROJECT_DIR / "core" / "apps.py", create_apps_py())
    create_file(PROJECT_DIR / "core" / "forms.py", create_forms_py())
    create_file(PROJECT_DIR / "core" / "decorators.py", create_decorators_py())
    create_file(PROJECT_DIR / "core" / "views.py", create_views_py())
    create_file(PROJECT_DIR / "core" / "urls.py", create_core_urls_py())
    
    # Escribir templates base
    print_step("Generando templates HTML...")
    create_file(TEMPLATES_DIR / "base.html", create_base_html())
    create_file(TEMPLATES_DIR / "index.html", create_index_html())
    create_file(TEMPLATES_DIR / "login.html", create_login_html())
    create_file(TEMPLATES_DIR / "registro.html", create_registro_html())
    create_file(TEMPLATES_DIR / "dashboard.html", create_dashboard_html())
    create_file(TEMPLATES_DIR / "examen_form.html", create_examen_form_html())
    create_file(TEMPLATES_DIR / "examen.html", create_examen_html())
    create_file(TEMPLATES_DIR / "admin_panel.html", create_admin_panel_html())
    create_file(TEMPLATES_DIR / "admin_nuevo_usuario.html", create_admin_nuevo_usuario_html())
    create_file(TEMPLATES_DIR / "proyecto.html", create_proyecto_html())
    
    # Crear templates para cada sección
    for section in SECTIONS:
        create_file(TEMPLATES_DIR / f"{section['name']}.html", create_section_template(section))
    
    # Crear manage.py y requirements.txt
    create_file(PROJECT_DIR / "manage.py", create_manage_py())
    create_file(PROJECT_DIR / "requirements.txt", create_requirements_txt())
    
    # Aviso sobre archivos JSON
    print_warning(f"Debes colocar los archivos JSON en {DATA_DIR}")
    print_warning("Archivos JSON necesarios:")
    for section in SECTIONS:
        print(f"  - {section['json_file']}")
    
    print_step("Ejecutando migraciones...")
    result, _, _ = run_command(f"{python_cmd} manage.py makemigrations")
    result, _, _ = run_command(f"{python_cmd} manage.py migrate")
    
    print_step("Creando superusuario...")
    print("  Ahora se te pedirá crear un superusuario para acceder al admin.")
    run_command(f"{python_cmd} manage.py createsuperuser", capture_output=False)
    
    print_header("INSTALACIÓN COMPLETADA")
    print(f"\n📁 Proyecto instalado en: {PROJECT_DIR}")
    print(f"🚀 Para iniciar el servidor:")
    print(f"   cd {PROJECT_DIR}")
    print(f"   source {VENV_DIR}/bin/activate  # Linux/Mac")
    print(f"   {VENV_DIR}\\Scripts\\activate  # Windows")
    print(f"   python manage.py runserver")
    print(f"\n🌐 Abre en tu navegador: http://127.0.0.1:8000")
    print(f"\n📌 Nota: Debes copiar manualmente los archivos JSON a {DATA_DIR}")
    
    # Preguntar si desea iniciar el servidor
    print("\n" + "-" * 50)
    respuesta = input("¿Deseas iniciar el servidor ahora? (s/n): ").lower()
    if respuesta == 's':
        print("\nIniciando servidor...")
        run_command(f"{python_cmd} manage.py runserver", capture_output=False)
    else:
        print("\nPuedes iniciar el servidor manualmente con los comandos indicados.")


if __name__ == "__main__":
    main()