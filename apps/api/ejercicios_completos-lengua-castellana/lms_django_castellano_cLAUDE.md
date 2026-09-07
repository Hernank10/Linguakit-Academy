# Plataforma LMS con Django para la Enseñanza del Castellano
## Guía Instructiva Completa: Arquitectura, i18n, Gamificación y Despliegue

---

## Índice

1. Visión General del Proyecto
2. Stack Tecnológico
3. Arquitectura del Sistema
4. Configuración del Proyecto Django
5. Internacionalización (i18n) — Las 20 Lenguas de Internet
6. Modelos de Datos
7. Panel de Administración (Admin)
8. Sistema de Autenticación (Login, Registro, Perfil)
9. Dashboard del Estudiante
10. Sistema de Cursos: Niveles A1 – C2
11. Motor de Progreso y Puntaje
12. Sistema de Medallas y Logros
13. API REST y Frontend
14. Despliegue en Producción
15. Conclusión

---

## 1. Visión General del Proyecto

Este ensayo describe paso a paso la construcción de una plataforma LMS (Learning Management System) orientada a la enseñanza de la **Lengua Castellana** desde su nivel más básico (A1) hasta el dominio avanzado (C2), siguiendo el Marco Común Europeo de Referencia para las Lenguas (MCER).

El público objetivo son los hablantes nativos de las **20 lenguas más habladas en internet**:

| # | Lengua         | # | Lengua        |
|---|----------------|---|---------------|
| 1 | Inglés (en)    | 11 | Holandés (nl) |
| 2 | Chino Mandarín (zh) | 12 | Turco (tr) |
| 3 | Español (es)\* | 13 | Italiano (it) |
| 4 | Árabe (ar)     | 14 | Tailandés (th) |
| 5 | Portugués (pt) | 15 | Vietnamita (vi) |
| 6 | Indonesio (id) | 16 | Polaco (pl) |
| 7 | Japonés (ja)   | 17 | Sueco (sv) |
| 8 | Ruso (ru)      | 18 | Griego (el) |
| 9 | Alemán (de)    | 19 | Checo (cs) |
| 10 | Francés (fr)   | 20 | Rumano (ro) |

\* La interfaz se adapta a hablantes no nativos de español.

### Funcionalidades Clave

- Registro y login con verificación por correo
- Perfil de usuario personalizable
- Panel de administración Django + Jazzmin
- Dashboard del estudiante con estadísticas en tiempo real
- Cursos estructurados por niveles A1, A2, B1, B2, C1 y C2
- Sistema de progreso por lección y por nivel
- Puntaje acumulable (XP — Experience Points)
- Medallas y logros desbloqueables (gamificación)
- Soporte completo de internacionalización (i18n / l10n)
- API REST para apps móviles futuras

---

## 2. Stack Tecnológico

```
Backend:       Django 5.x + Django REST Framework
Base de datos: PostgreSQL 16
Cache / Colas: Redis + Celery
Frontend:      Django Templates + HTMX + Alpine.js + Tailwind CSS
i18n:          Django i18n + Rosetta + gettext
Autenticación: django-allauth
Admin:         Jazzmin (tema moderno para Django Admin)
Almacenamiento: AWS S3 / Cloudflare R2 (media files)
Despliegue:    Docker + Nginx + Gunicorn + VPS / Railway / Render
```

---

## 3. Arquitectura del Sistema

```
lms_castellano/
├── config/                  # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/            # Autenticación, registro, perfil
│   ├── courses/             # Cursos, lecciones, niveles MCER
│   ├── progress/            # Progreso del estudiante
│   ├── gamification/        # Puntos XP, medallas, logros
│   ├── dashboard/           # Vistas del dashboard
│   └── core/                # Modelos base, utilidades
├── locale/                  # Archivos .po / .mo de traducción
│   ├── en/LC_MESSAGES/
│   ├── zh/LC_MESSAGES/
│   ├── ar/LC_MESSAGES/
│   └── ...  (20 idiomas)
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── courses/
│   ├── dashboard/
│   └── gamification/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── docker-compose.yml
└── manage.py
```

---

## 4. Configuración del Proyecto Django

### 4.1 Instalación inicial

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias base
pip install django==5.1 \
            djangorestframework \
            django-allauth \
            jazzmin \
            django-rosetta \
            Pillow \
            psycopg2-binary \
            redis \
            celery \
            django-htmx \
            whitenoise

# Crear proyecto
django-admin startproject config .

# Crear aplicaciones
python manage.py startapp accounts
python manage.py startapp courses
python manage.py startapp progress
python manage.py startapp gamification
python manage.py startapp dashboard
python manage.py startapp core
```

### 4.2 settings/base.py

```python
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    # Jazzmin DEBE ir antes de django.contrib.admin
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rosetta',

    # Apps propias
    'apps.accounts',
    'apps.courses',
    'apps.progress',
    'apps.gamification',
    'apps.dashboard',
    'apps.core',
]

# ─── Internacionalización ───────────────────────────────────────────
LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
    ('zh-hans', _('中文')),
    ('ar', _('العربية')),
    ('pt', _('Português')),
    ('id', _('Bahasa Indonesia')),
    ('ja', _('日本語')),
    ('ru', _('Русский')),
    ('de', _('Deutsch')),
    ('fr', _('Français')),
    ('nl', _('Nederlands')),
    ('tr', _('Türkçe')),
    ('it', _('Italiano')),
    ('th', _('ภาษาไทย')),
    ('vi', _('Tiếng Việt')),
    ('pl', _('Polski')),
    ('sv', _('Svenska')),
    ('el', _('Ελληνικά')),
    ('cs', _('Čeština')),
    ('ro', _('Română')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # LocaleMiddleware DEBE ir después de SessionMiddleware
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# ─── Jazzmin (Admin) ────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "LMS Castellano Admin",
    "site_header": "Castellano LMS",
    "site_brand": "🇪🇸 Aprende Castellano",
    "welcome_sign": "Bienvenido al Panel de Administración",
    "topmenu_links": [
        {"name": "Ver Sitio", "url": "home", "new_window": False},
        {"model": "auth.user"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "courses.course": "fas fa-book",
        "courses.lesson": "fas fa-file-alt",
        "gamification.badge": "fas fa-medal",
        "progress.studentprogress": "fas fa-chart-line",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "css/admin_custom.css",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
}

# ─── Autenticación (django-allauth) ─────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'home'
```

---

## 5. Internacionalización (i18n) — Las 20 Lenguas de Internet

### 5.1 Generar archivos de traducción

```bash
# Crear los mensajes para todos los idiomas
django-admin makemessages --all --extension=html,py,txt

# Estructura resultante:
# locale/
#   en/LC_MESSAGES/django.po
#   zh_Hans/LC_MESSAGES/django.po
#   ar/LC_MESSAGES/django.po
#   ...

# Después de traducir, compilar:
django-admin compilemessages
```

### 5.2 Uso en templates

```html
{% load i18n %}

<!-- Cadena simple -->
<h1>{% trans "Aprende Castellano" %}</h1>

<!-- Con variable -->
<p>{% blocktrans with level=course.level %}
    Estás en el nivel {{ level }}
{% endblocktrans %}</p>

<!-- Selector de idioma -->
<form action="{% url 'set_language' %}" method="post">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ redirect_to }}">
    <select name="language" onchange="this.form.submit()">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% for lang_code, lang_name in LANGUAGES %}
            <option value="{{ lang_code }}"
                {% if lang_code == LANGUAGE_CODE %}selected{% endif %}>
                {{ lang_name }}
            </option>
        {% endfor %}
    </select>
</form>
```

### 5.3 Uso en Python

```python
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

class Course(models.Model):
    title = models.CharField(
        _("título del curso"),
        max_length=200
    )
    description = models.TextField(_("descripción"))

def get_lesson_count_text(count):
    return ngettext(
        "%(count)d lección disponible",
        "%(count)d lecciones disponibles",
        count
    ) % {'count': count}
```

### 5.4 Rosetta para gestión de traducciones

```python
# Añadir en urls.py del proyecto
if settings.DEBUG:
    import rosetta
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]
```

Rosetta provee una interfaz web amigable en `/rosetta/` donde traductores pueden gestionar los textos sin tocar archivos `.po` directamente.

---

## 6. Modelos de Datos

### 6.1 apps/accounts/models.py

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Usuario extendido con datos del estudiante."""

    NATIVE_LANGUAGE_CHOICES = [
        ('en', 'English'), ('zh', '中文'), ('ar', 'العربية'),
        ('pt', 'Português'), ('id', 'Bahasa Indonesia'),
        ('ja', '日本語'), ('ru', 'Русский'), ('de', 'Deutsch'),
        ('fr', 'Français'), ('nl', 'Nederlands'), ('tr', 'Türkçe'),
        ('it', 'Italiano'), ('th', 'ภาษาไทย'), ('vi', 'Tiếng Việt'),
        ('pl', 'Polski'), ('sv', 'Svenska'), ('el', 'Ελληνικά'),
        ('cs', 'Čeština'), ('ro', 'Română'), ('es', 'Español'),
    ]

    email = models.EmailField(_("correo electrónico"), unique=True)
    native_language = models.CharField(
        _("lengua materna"),
        max_length=10,
        choices=NATIVE_LANGUAGE_CHOICES,
        default='en'
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    bio = models.TextField(_("biografía"), blank=True)
    country = models.CharField(_("país"), max_length=100, blank=True)
    total_xp = models.PositiveIntegerField(_("puntos XP totales"), default=0)
    streak_days = models.PositiveIntegerField(_("racha de días"), default=0)
    last_activity = models.DateField(_("última actividad"), null=True, blank=True)
    interface_language = models.CharField(
        _("idioma de la interfaz"),
        max_length=10,
        default='en'
    )
    current_level = models.CharField(
        _("nivel actual MCER"),
        max_length=2,
        choices=[('A1','A1'),('A2','A2'),('B1','B1'),
                 ('B2','B2'),('C1','C1'),('C2','C2')],
        default='A1'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")

    def __str__(self):
        return f"{self.username} ({self.get_current_level_display()})"
```

### 6.2 apps/courses/models.py

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Level(TimeStampedModel):
    """Nivel MCER: A1, A2, B1, B2, C1, C2."""

    LEVEL_CHOICES = [
        ('A1', _('A1 — Acceso')),
        ('A2', _('A2 — Plataforma')),
        ('B1', _('B1 — Umbral')),
        ('B2', _('B2 — Avanzado')),
        ('C1', _('C1 — Dominio operativo eficaz')),
        ('C2', _('C2 — Maestría')),
    ]

    code = models.CharField(max_length=2, choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(_("nombre"), max_length=100)
    description = models.TextField(_("descripción"))
    order = models.PositiveSmallIntegerField(_("orden"), unique=True)
    xp_required = models.PositiveIntegerField(
        _("XP requeridos para acceder"), default=0
    )
    color_hex = models.CharField(
        _("color representativo"), max_length=7, default='#3B82F6'
    )

    class Meta:
        ordering = ['order']
        verbose_name = _("nivel")
        verbose_name_plural = _("niveles")

    def __str__(self):
        return self.code


class Course(TimeStampedModel):
    """Curso perteneciente a un nivel MCER."""

    level = models.ForeignKey(
        Level, on_delete=models.CASCADE,
        related_name='courses', verbose_name=_("nivel")
    )
    title = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("descripción"))
    thumbnail = models.ImageField(
        _("miniatura"), upload_to='courses/thumbnails/', null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(_("orden"))
    is_published = models.BooleanField(_("publicado"), default=False)
    xp_reward = models.PositiveIntegerField(_("XP al completar"), default=100)
    estimated_hours = models.DecimalField(
        _("horas estimadas"), max_digits=4, decimal_places=1, default=2.0
    )

    class Meta:
        ordering = ['level__order', 'order']
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")


class Lesson(TimeStampedModel):
    """Lección dentro de un curso."""

    LESSON_TYPE_CHOICES = [
        ('vocabulary',   _('Vocabulario')),
        ('grammar',      _('Gramática')),
        ('reading',      _('Lectura')),
        ('writing',      _('Escritura')),
        ('listening',    _('Comprensión auditiva')),
        ('pronunciation',_('Pronunciación')),
        ('quiz',         _('Evaluación')),
    ]

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='lessons', verbose_name=_("curso")
    )
    title = models.CharField(_("título"), max_length=200)
    slug = models.SlugField()
    lesson_type = models.CharField(
        _("tipo de lección"), max_length=20,
        choices=LESSON_TYPE_CHOICES, default='vocabulary'
    )
    content = models.TextField(_("contenido"))
    order = models.PositiveSmallIntegerField(_("orden"))
    xp_reward = models.PositiveIntegerField(_("XP al completar"), default=20)
    is_published = models.BooleanField(_("publicada"), default=False)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'slug']


class Exercise(TimeStampedModel):
    """Ejercicio interactivo dentro de una lección."""

    EXERCISE_TYPE_CHOICES = [
        ('multiple_choice', _('Opción múltiple')),
        ('fill_blank',      _('Rellenar huecos')),
        ('translation',     _('Traducción')),
        ('dictation',       _('Dictado')),
        ('reorder',         _('Ordenar palabras')),
        ('match',           _('Emparejar')),
    ]

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='exercises', verbose_name=_("lección")
    )
    exercise_type = models.CharField(
        _("tipo"), max_length=20, choices=EXERCISE_TYPE_CHOICES
    )
    question = models.TextField(_("pregunta / instrucción"))
    correct_answer = models.TextField(_("respuesta correcta"))
    options = models.JSONField(
        _("opciones (JSON)"), default=list, blank=True
    )
    explanation = models.TextField(_("explicación"), blank=True)
    xp_reward = models.PositiveIntegerField(_("XP al acertar"), default=5)
    order = models.PositiveSmallIntegerField(_("orden"))

    class Meta:
        ordering = ['order']
```

### 6.3 apps/progress/models.py

```python
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class CourseEnrollment(TimeStampedModel):
    """Inscripción de un usuario en un curso."""

    STATUS_CHOICES = [
        ('active',    _('Activo')),
        ('completed', _('Completado')),
        ('paused',    _('Pausado')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE
    )
    status = models.CharField(
        _("estado"), max_length=10,
        choices=STATUS_CHOICES, default='active'
    )
    progress_percent = models.DecimalField(
        _("porcentaje completado"), max_digits=5,
        decimal_places=2, default=0.00
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']

    def update_progress(self):
        total = self.course.lessons.filter(is_published=True).count()
        if total == 0:
            return
        done = LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            is_completed=True
        ).count()
        self.progress_percent = (done / total) * 100
        if self.progress_percent >= 100:
            from django.utils import timezone
            self.status = 'completed'
            self.completed_at = timezone.now()
        self.save()


class LessonProgress(TimeStampedModel):
    """Registro del progreso de una lección específica."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='lesson_progresses'
    )
    lesson = models.ForeignKey(
        'courses.Lesson', on_delete=models.CASCADE
    )
    is_completed = models.BooleanField(_("completada"), default=False)
    score = models.PositiveSmallIntegerField(_("puntuación"), default=0)
    attempts = models.PositiveSmallIntegerField(_("intentos"), default=0)
    time_spent_seconds = models.PositiveIntegerField(
        _("tiempo invertido (seg)"), default=0
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'lesson']
```

### 6.4 apps/gamification/models.py

```python
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Badge(TimeStampedModel):
    """Medalla / Insignia."""

    CATEGORY_CHOICES = [
        ('level',     _('Nivel')),
        ('streak',    _('Racha')),
        ('speed',     _('Velocidad')),
        ('perfect',   _('Perfección')),
        ('social',    _('Social')),
        ('milestone', _('Hito')),
    ]

    name = models.CharField(_("nombre"), max_length=100)
    description = models.TextField(_("descripción"))
    icon = models.ImageField(
        _("ícono"), upload_to='badges/', null=True, blank=True
    )
    icon_emoji = models.CharField(
        _("emoji del ícono"), max_length=10, default='🏅'
    )
    category = models.CharField(
        _("categoría"), max_length=20, choices=CATEGORY_CHOICES
    )
    xp_bonus = models.PositiveIntegerField(_("XP bonus"), default=0)
    condition_type = models.CharField(
        _("tipo de condición"), max_length=50
    )
    condition_value = models.PositiveIntegerField(
        _("valor de la condición")
    )
    is_active = models.BooleanField(_("activa"), default=True)

    class Meta:
        verbose_name = _("medalla")
        verbose_name_plural = _("medallas")

    def __str__(self):
        return f"{self.icon_emoji} {self.name}"


class UserBadge(TimeStampedModel):
    """Medalla obtenida por un usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='badges'
    )
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='earned_by'
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        verbose_name = _("medalla del usuario")

    def __str__(self):
        return f"{self.user.username} — {self.badge.name}"


class XPTransaction(TimeStampedModel):
    """Historial de puntos XP ganados."""

    REASON_CHOICES = [
        ('lesson_complete',  _('Lección completada')),
        ('course_complete',  _('Curso completado')),
        ('exercise_correct', _('Ejercicio correcto')),
        ('daily_streak',     _('Racha diaria')),
        ('badge_earned',     _('Medalla obtenida')),
        ('level_up',         _('Subida de nivel')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='xp_transactions'
    )
    amount = models.IntegerField(_("cantidad XP"))
    reason = models.CharField(
        _("razón"), max_length=30, choices=REASON_CHOICES
    )
    description = models.CharField(_("descripción"), max_length=200, blank=True)
    reference_id = models.PositiveIntegerField(
        _("ID de referencia"), null=True, blank=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("transacción XP")
```

---

## 7. Panel de Administración (Admin)

### 7.1 Registro de modelos

```python
# apps/courses/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Level, Course, Lesson, Exercise


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'lesson_type', 'order', 'xp_reward', 'is_published']
    ordering = ['order']


class ExerciseInline(admin.StackedInline):
    model = Exercise
    extra = 1
    fields = ['exercise_type', 'question', 'correct_answer',
              'options', 'explanation', 'xp_reward', 'order']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order', 'xp_required']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'order', 'is_published',
                    'xp_reward', 'estimated_hours']
    list_filter = ['level', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    list_editable = ['is_published', 'order']

    fieldsets = (
        (_('Información básica'), {
            'fields': ('level', 'title', 'slug', 'description', 'thumbnail')
        }),
        (_('Configuración'), {
            'fields': ('order', 'is_published', 'xp_reward', 'estimated_hours')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson_type', 'order',
                    'xp_reward', 'is_published']
    list_filter = ['course__level', 'lesson_type', 'is_published']
    search_fields = ['title', 'content']
    inlines = [ExerciseInline]
```

```python
# apps/gamification/admin.py
from django.contrib import admin
from .models import Badge, UserBadge, XPTransaction


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon_emoji', 'name', 'category', 'xp_bonus',
                    'condition_type', 'condition_value', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge__category']
    search_fields = ['user__username', 'badge__name']
    raw_id_fields = ['user']


@admin.register(XPTransaction)
class XPTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'description', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
```

---

## 8. Sistema de Autenticación

### 8.1 Registro personalizado

```python
# apps/accounts/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    native_language = forms.ChoiceField(
        choices=User.NATIVE_LANGUAGE_CHOICES,
        label=_("Tu lengua materna"),
        help_text=_("Esto nos ayuda a personalizar tu experiencia")
    )
    first_name = forms.CharField(
        max_length=50, label=_("Nombre")
    )
    last_name = forms.CharField(
        max_length=50, label=_("Apellido"), required=False
    )
    accept_terms = forms.BooleanField(
        label=_("Acepto los términos y condiciones"),
        error_messages={'required': _("Debes aceptar los términos.")}
    )

    def save(self, request):
        user = super().save(request)
        user.native_language = self.cleaned_data['native_language']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        user.save()
        return user
```

```python
# config/settings/base.py
ACCOUNT_FORMS = {'signup': 'apps.accounts.forms.CustomSignupForm'}
```

### 8.2 Template de login (templates/account/login.html)

```html
{% extends "base.html" %}
{% load i18n %}

{% block content %}
<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800">🇪🇸</h1>
            <h2 class="text-2xl font-bold text-gray-800 mt-2">
                {% trans "Iniciar sesión" %}
            </h2>
            <p class="text-gray-500 mt-1">
                {% trans "Continúa tu aprendizaje del castellano" %}
            </p>
        </div>

        <form method="post" class="space-y-5">
            {% csrf_token %}
            {{ form.as_div }}
            <button type="submit"
                class="w-full bg-indigo-600 hover:bg-indigo-700 text-white
                       font-semibold py-3 rounded-xl transition duration-200">
                {% trans "Entrar" %}
            </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
            {% trans "¿No tienes cuenta?" %}
            <a href="{% url 'account_signup' %}"
               class="text-indigo-600 hover:underline font-medium">
                {% trans "Regístrate gratis" %}
            </a>
        </p>
    </div>
</div>
{% endblock %}
```

### 8.3 Vista de perfil

```python
# apps/accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'bio', 'avatar',
              'country', 'native_language', 'interface_language']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = _("Mi Perfil")
        ctx['badges'] = self.request.user.badges.select_related('badge').all()
        ctx['total_courses'] = self.request.user.enrollments.count()
        ctx['completed_courses'] = self.request.user.enrollments.filter(
            status='completed'
        ).count()
        return ctx
```

---

## 9. Dashboard del Estudiante

### 9.1 Vista del dashboard

```python
# apps/dashboard/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from apps.courses.models import Level, Course
from apps.progress.models import CourseEnrollment, LessonProgress
from apps.gamification.models import UserBadge, XPTransaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Cursos activos
        ctx['active_enrollments'] = CourseEnrollment.objects.filter(
            user=user, status='active'
        ).select_related('course', 'course__level').order_by('-updated_at')[:5]

        # Estadísticas
        ctx['stats'] = {
            'total_xp': user.total_xp,
            'streak_days': user.streak_days,
            'completed_courses': CourseEnrollment.objects.filter(
                user=user, status='completed'
            ).count(),
            'lessons_done': LessonProgress.objects.filter(
                user=user, is_completed=True
            ).count(),
            'badges_earned': UserBadge.objects.filter(user=user).count(),
        }

        # Últimas transacciones XP
        ctx['recent_xp'] = XPTransaction.objects.filter(
            user=user
        ).order_by('-created_at')[:5]

        # Cursos recomendados (del nivel actual)
        ctx['recommended_courses'] = Course.objects.filter(
            level__code=user.current_level,
            is_published=True
        ).exclude(
            id__in=CourseEnrollment.objects.filter(user=user).values('course_id')
        )[:3]

        # Progreso por nivel
        ctx['levels'] = Level.objects.all()
        ctx['current_level'] = user.current_level

        ctx['title'] = _("Mi Panel de Aprendizaje")
        return ctx
```

### 9.2 Template del dashboard (fragmento)

```html
{% extends "base.html" %}
{% load i18n humanize %}

{% block content %}
<div class="container mx-auto px-4 py-8">

    <!-- Bienvenida y XP -->
    <div class="bg-gradient-to-r from-indigo-600 to-purple-600
                rounded-2xl p-6 text-white mb-8 flex items-center
                justify-between">
        <div>
            <h1 class="text-2xl font-bold">
                {% blocktrans with name=request.user.first_name %}
                    ¡Hola, {{ name }}!
                {% endblocktrans %}
            </h1>
            <p class="opacity-80 mt-1">
                {% trans "Nivel actual:" %} <strong>{{ current_level }}</strong>
            </p>
        </div>
        <div class="text-right">
            <div class="text-4xl font-black">{{ stats.total_xp|intcomma }}</div>
            <div class="text-sm opacity-75">{% trans "Puntos XP" %}</div>
        </div>
    </div>

    <!-- Tarjetas de estadísticas -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="stat-card">
            <div class="text-3xl">🔥</div>
            <div class="text-2xl font-bold">{{ stats.streak_days }}</div>
            <div class="text-sm text-gray-500">{% trans "Días seguidos" %}</div>
        </div>
        <div class="stat-card">
            <div class="text-3xl">📚</div>
            <div class="text-2xl font-bold">{{ stats.completed_courses }}</div>
            <div class="text-sm text-gray-500">{% trans "Cursos completados" %}</div>
        </div>
        <div class="stat-card">
            <div class="text-3xl">✅</div>
            <div class="text-2xl font-bold">{{ stats.lessons_done }}</div>
            <div class="text-sm text-gray-500">{% trans "Lecciones hechas" %}</div>
        </div>
        <div class="stat-card">
            <div class="text-3xl">🏅</div>
            <div class="text-2xl font-bold">{{ stats.badges_earned }}</div>
            <div class="text-sm text-gray-500">{% trans "Medallas" %}</div>
        </div>
    </div>

    <!-- Cursos activos con barra de progreso -->
    <h2 class="text-xl font-bold text-gray-800 mb-4">
        {% trans "Continúa aprendiendo" %}
    </h2>
    <div class="grid md:grid-cols-2 gap-6 mb-8">
        {% for enrollment in active_enrollments %}
        <a href="{% url 'courses:detail' enrollment.course.slug %}"
           class="course-card group hover:shadow-lg transition-all">
            <div class="flex justify-between items-start mb-3">
                <div>
                    <span class="badge-level">{{ enrollment.course.level.code }}</span>
                    <h3 class="font-semibold text-gray-800 mt-1">
                        {{ enrollment.course.title }}
                    </h3>
                </div>
                <span class="text-indigo-600 font-bold">
                    {{ enrollment.progress_percent|floatformat:0 }}%
                </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-indigo-500 h-2 rounded-full transition-all"
                     style="width: {{ enrollment.progress_percent }}%"></div>
            </div>
        </a>
        {% empty %}
        <p class="text-gray-500 col-span-2">
            {% trans "Aún no estás inscrito en ningún curso." %}
            <a href="{% url 'courses:list' %}" class="text-indigo-600 underline">
                {% trans "Explorar cursos" %}
            </a>
        </p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

---

## 10. Sistema de Cursos: Niveles A1 – C2

### 10.1 Vista de catálogo de cursos

```python
# apps/courses/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from .models import Level, Course, Lesson


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True)\
                           .select_related('level')\
                           .prefetch_related('lessons')

        level_filter = self.request.GET.get('level')
        if level_filter:
            qs = qs.filter(level__code=level_filter)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['levels'] = Level.objects.all()
        ctx['selected_level'] = self.request.GET.get('level', '')
        ctx['title'] = _("Catálogo de cursos de Castellano")

        # Marcar cursos ya inscritos
        if self.request.user.is_authenticated:
            enrolled_ids = set(
                self.request.user.enrollments.values_list('course_id', flat=True)
            )
            for course in ctx['courses']:
                course.is_enrolled = course.id in enrolled_ids
        return ctx


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson.html'
    slug_url_kwarg = 'lesson_slug'

    def get_queryset(self):
        return Lesson.objects.filter(
            course__slug=self.kwargs['course_slug'],
            is_published=True
        ).prefetch_related('exercises')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lesson = self.object
        user = self.request.user

        # Progreso de esta lección
        from apps.progress.models import LessonProgress
        progress, _ = LessonProgress.objects.get_or_create(
            user=user, lesson=lesson
        )
        ctx['progress'] = progress

        # Lección anterior y siguiente
        siblings = lesson.course.lessons.filter(is_published=True)
        ctx['prev_lesson'] = siblings.filter(order__lt=lesson.order).last()
        ctx['next_lesson'] = siblings.filter(order__gt=lesson.order).first()
        return ctx
```

### 10.2 Estructura de contenidos por nivel

```
NIVELES Y CURSOS SUGERIDOS
══════════════════════════════════════════════════════════════════

A1 — ACCESO
  ├── Curso 1: Saludos y presentaciones
  ├── Curso 2: Números, colores y objetos cotidianos
  ├── Curso 3: La familia y las personas
  └── Curso 4: Verbo ser/estar — introducción

A2 — PLATAFORMA
  ├── Curso 1: Rutinas diarias y tiempo libre
  ├── Curso 2: Compras y precios
  ├── Curso 3: Presente de indicativo — verbos irregulares
  └── Curso 4: Descripción de lugares

B1 — UMBRAL
  ├── Curso 1: Pasado simple y pasado imperfecto
  ├── Curso 2: Expresar opiniones y sentimientos
  ├── Curso 3: Medios de comunicación y tecnología
  └── Curso 4: Escritura de correos formales e informales

B2 — AVANZADO
  ├── Curso 1: Subjuntivo — usos y contextos
  ├── Curso 2: Textos académicos y argumentativos
  ├── Curso 3: Variedades del español (Latinoamérica, España)
  └── Curso 4: Comprensión de textos literarios

C1 — DOMINIO OPERATIVO EFICAZ
  ├── Curso 1: Expresión escrita avanzada
  ├── Curso 2: Registro formal — ámbito profesional
  ├── Curso 3: Matices y modismos del castellano
  └── Curso 4: Análisis crítico de textos

C2 — MAESTRÍA
  ├── Curso 1: Escritura creativa y estilo
  ├── Curso 2: Literatura hispanoamericana
  ├── Curso 3: Ortografía y gramática normativa avanzada
  └── Curso 4: Evaluación final DELE C2 (simulacro)
```

---

## 11. Motor de Progreso y Puntaje

### 11.1 Servicio de XP

```python
# apps/gamification/services.py
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import XPTransaction, Badge, UserBadge
from apps.progress.models import CourseEnrollment, LessonProgress


class XPService:
    """Servicio centralizado para otorgar puntos XP y verificar medallas."""

    @staticmethod
    @transaction.atomic
    def award_xp(user, amount: int, reason: str,
                 description: str = '', reference_id: int = None):
        """Otorga XP al usuario y verifica si ganó nuevas medallas."""
        if amount <= 0:
            return

        # Registrar transacción
        XPTransaction.objects.create(
            user=user,
            amount=amount,
            reason=reason,
            description=description,
            reference_id=reference_id
        )

        # Actualizar XP total
        user.total_xp = (user.total_xp or 0) + amount
        user.save(update_fields=['total_xp'])

        # Verificar medallas
        BadgeService.check_and_award_badges(user)

    @staticmethod
    def update_streak(user):
        """Actualiza la racha diaria del usuario."""
        today = timezone.now().date()
        last = user.last_activity

        if last is None or (today - last).days > 1:
            user.streak_days = 1
        elif (today - last).days == 1:
            user.streak_days += 1
            # Bonificación por racha
            if user.streak_days % 7 == 0:
                XPService.award_xp(
                    user, 50, 'daily_streak',
                    description=f"Racha de {user.streak_days} días"
                )

        user.last_activity = today
        user.save(update_fields=['streak_days', 'last_activity'])


class BadgeService:
    """Servicio para verificar y otorgar medallas automáticamente."""

    @staticmethod
    def check_and_award_badges(user):
        """Revisa todas las medallas activas y otorga las que apliquen."""
        already_earned = set(
            UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        )
        candidates = Badge.objects.filter(is_active=True)\
                                  .exclude(id__in=already_earned)

        for badge in candidates:
            if BadgeService._meets_condition(user, badge):
                UserBadge.objects.create(user=user, badge=badge)
                # XP bonus por la medalla
                if badge.xp_bonus > 0:
                    XPTransaction.objects.create(
                        user=user, amount=badge.xp_bonus,
                        reason='badge_earned',
                        description=f"Medalla: {badge.name}",
                        reference_id=badge.id
                    )
                    user.total_xp += badge.xp_bonus
                    user.save(update_fields=['total_xp'])

    @staticmethod
    def _meets_condition(user, badge) -> bool:
        """Evalúa si el usuario cumple la condición de la medalla."""
        ct = badge.condition_type
        cv = badge.condition_value

        conditions = {
            'total_xp':          lambda: user.total_xp >= cv,
            'streak_days':       lambda: user.streak_days >= cv,
            'lessons_completed': lambda: LessonProgress.objects.filter(
                                     user=user, is_completed=True
                                 ).count() >= cv,
            'courses_completed': lambda: CourseEnrollment.objects.filter(
                                     user=user, status='completed'
                                 ).count() >= cv,
            'perfect_score':     lambda: LessonProgress.objects.filter(
                                     user=user, score=100
                                 ).count() >= cv,
        }

        handler = conditions.get(ct)
        return handler() if handler else False
```

### 11.2 Señales para actualización automática

```python
# apps/progress/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.gamification.services import XPService
from .models import LessonProgress


@receiver(post_save, sender=LessonProgress)
def on_lesson_completed(sender, instance, created, **kwargs):
    if instance.is_completed:
        lesson = instance.lesson
        user = instance.user

        # Otorgar XP de la lección
        XPService.award_xp(
            user=user,
            amount=lesson.xp_reward,
            reason='lesson_complete',
            description=f'Lección: {lesson.title}',
            reference_id=lesson.id
        )

        # Actualizar progreso del curso
        enrollment = user.enrollments.filter(
            course=lesson.course
        ).first()
        if enrollment:
            enrollment.update_progress()

            # Si el curso se completó, dar XP del curso
            if enrollment.status == 'completed':
                XPService.award_xp(
                    user=user,
                    amount=lesson.course.xp_reward,
                    reason='course_complete',
                    description=f'Curso: {lesson.course.title}',
                    reference_id=lesson.course.id
                )

        # Actualizar racha
        XPService.update_streak(user)
```

---

## 12. Sistema de Medallas y Logros

### 12.1 Medallas predefinidas (fixture)

```json
[
  {
    "model": "gamification.badge",
    "pk": 1,
    "fields": {
      "name": "Primer Paso",
      "description": "Completaste tu primera lección de castellano.",
      "icon_emoji": "👣",
      "category": "milestone",
      "xp_bonus": 25,
      "condition_type": "lessons_completed",
      "condition_value": 1,
      "is_active": true
    }
  },
  {
    "model": "gamification.badge",
    "pk": 2,
    "fields": {
      "name": "Racha de Fuego",
      "description": "7 días consecutivos de práctica.",
      "icon_emoji": "🔥",
      "category": "streak",
      "xp_bonus": 75,
      "condition_type": "streak_days",
      "condition_value": 7,
      "is_active": true
    }
  },
  {
    "model": "gamification.badge",
    "pk": 3,
    "fields": {
      "name": "Estudiante A1",
      "description": "Completaste todos los cursos del nivel A1.",
      "icon_emoji": "🎓",
      "category": "level",
      "xp_bonus": 200,
      "condition_type": "courses_completed",
      "condition_value": 4,
      "is_active": true
    }
  },
  {
    "model": "gamification.badge",
    "pk": 4,
    "fields": {
      "name": "Perfeccionista",
      "description": "Obtuviste 100/100 en 10 lecciones.",
      "icon_emoji": "💎",
      "category": "perfect",
      "xp_bonus": 150,
      "condition_type": "perfect_score",
      "condition_value": 10,
      "is_active": true
    }
  },
  {
    "model": "gamification.badge",
    "pk": 5,
    "fields": {
      "name": "Maestro del Castellano",
      "description": "Acumulaste 10,000 puntos XP.",
      "icon_emoji": "👑",
      "category": "milestone",
      "xp_bonus": 500,
      "condition_type": "total_xp",
      "condition_value": 10000,
      "is_active": true
    }
  }
]
```

```bash
# Cargar las medallas iniciales
python manage.py loaddata badges.json
```

### 12.2 Vista de medallas del usuario

```python
# apps/gamification/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Badge, UserBadge


class BadgesView(LoginRequiredMixin, TemplateView):
    template_name = 'gamification/badges.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        earned_ids = set(
            UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        )

        all_badges = Badge.objects.filter(is_active=True)
        ctx['badges'] = [
            {
                'badge': b,
                'earned': b.id in earned_ids,
                'earned_at': UserBadge.objects.filter(
                    user=user, badge=b
                ).values_list('earned_at', flat=True).first()
            }
            for b in all_badges
        ]
        ctx['earned_count'] = len(earned_ids)
        ctx['total_count'] = all_badges.count()
        return ctx
```

---

## 13. API REST y Frontend

### 13.1 Serializers básicos

```python
# apps/courses/serializers.py
from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    level_code = serializers.CharField(source='level.code', read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description',
                  'level_code', 'xp_reward', 'estimated_hours', 'lesson_count']

    def get_lesson_count(self, obj):
        return obj.lessons.filter(is_published=True).count()


class LessonSerializer(serializers.ModelSerializer):
    exercises_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'lesson_type',
                  'xp_reward', 'exercises_count']

    def get_exercises_count(self, obj):
        return obj.exercises.count()
```

### 13.2 ViewSets

```python
# apps/courses/api_views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_published=True).select_related('level')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        level = self.request.query_params.get('level')
        if level:
            qs = qs.filter(level__code=level)
        return qs

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = course.lessons.filter(is_published=True)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
```

### 13.3 URLs del proyecto

```python
# config/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from rest_framework.routers import DefaultRouter
from apps.courses.api_views import CourseViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)

# URLs sin prefijo de idioma (API, admin)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs CON prefijo de idioma (/en/, /fr/, /zh/, etc.)
urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('courses/', include('apps.courses.urls')),
    path('gamification/', include('apps.gamification.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import rosetta
    urlpatterns += [path('rosetta/', include('rosetta.urls'))]
```

---

## 14. Despliegue en Producción

### 14.1 Docker Compose

```yaml
# docker-compose.yml
version: '3.9'

services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: lms_castellano
      POSTGRES_USER: lms_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://lms_user:${DB_PASSWORD}@db:5432/lms_castellano
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A config worker -l info
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    depends_on:
      - redis
      - db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

### 14.2 settings/production.py

```python
from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ['REDIS_URL'],
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_API_KEY']
DEFAULT_FROM_EMAIL = 'noreply@lmscastellano.com'

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 14.3 Comandos de despliegue

```bash
# Primera vez
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py loaddata badges.json

# Generar y compilar traducciones
docker-compose exec web python manage.py makemessages --all
# (traducir los .po con Rosetta o DeepL API)
docker-compose exec web python manage.py compilemessages

# Actualizar (zero downtime)
git pull
docker-compose build web
docker-compose up -d --no-deps web
docker-compose exec web python manage.py migrate
```

---

## 15. Conclusión

Esta plataforma LMS construida con Django representa una solución robusta, escalable y completamente internacionalizada para la enseñanza de la Lengua Castellana en el entorno digital global.

### Resumen de capacidades implementadas

| Módulo | Funcionalidad |
|--------|--------------|
| **Admin (Jazzmin)** | Gestión completa de contenidos, usuarios, medallas y estadísticas con interfaz moderna |
| **Autenticación** | Registro con verificación por email, login seguro, perfil personalizable, soporte OAuth |
| **i18n** | 20 idiomas soportados con LocaleMiddleware, archivos .po y Rosetta para traductores |
| **Cursos** | 6 niveles MCER (A1–C2), lecciones multimedia, 6 tipos de ejercicios interactivos |
| **Progreso** | Seguimiento por lección y curso, porcentajes en tiempo real, historial de actividad |
| **Puntaje (XP)** | Sistema de puntos con transacciones auditables, bonificaciones por racha y medallas |
| **Medallas** | 5+ tipos de logros desbloqueables automáticamente, con bonus de XP |
| **Dashboard** | Panel visual con estadísticas, cursos activos, recomendaciones y racha diaria |
| **API REST** | Endpoints listos para apps móviles con DRF |
| **Despliegue** | Docker + Nginx + Gunicorn + PostgreSQL + Redis + Celery |

### Próximos pasos recomendados

- Integrar DeepL API para traducción automática de contenidos durante la creación
- Añadir videolecciones con almacenamiento en Cloudflare Stream
- Implementar exámenes cronometrados con antifraude básico
- Añadir un foro comunitario por nivel con moderación automática
- Desarrollar la app móvil consumiendo la API REST existente
- Integrar IA (Claude API) para corrección automatizada de ejercicios de escritura libre

---

*Este ensayo instructivo cubre la arquitectura completa de una plataforma LMS profesional con Django. Cada sección es un punto de partida; el código mostrado está diseñado para ser extendido y adaptado según las necesidades específicas del proyecto.*
