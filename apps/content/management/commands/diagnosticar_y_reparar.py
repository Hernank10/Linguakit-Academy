import sys
import re
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.db.models import Count, Q
from django.test import Client
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured

# Importar modelos
from apps.content.models import (
    LinguisticTechnique, Curso, Leccion, Ejercicio, Evaluacion,
    ProgresoEstudiante, Certificado, RespuestaEjercicio
)
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = 'Diagnostica, corrige, completa y prueba todo el sistema LMS'

    def add_arguments(self, parser):
        parser.add_argument('--fix', action='store_true', help='Corregir automáticamente los problemas encontrados')
        parser.add_argument('--generate', action='store_true', help='Completar datos faltantes (cursos, lecciones, ejercicios, evaluaciones)')
        parser.add_argument('--test', action='store_true', help='Ejecutar pruebas de integración (simular navegación)')
        parser.add_argument('--full', action='store_true', help='Ejecutar todas las acciones (fix + generate + test)')

    @transaction.atomic
    def handle(self, *args, **options):
        fix = options['fix']
        generate = options['generate']
        test = options['test']
        full = options['full']

        if full:
            fix = True
            generate = True
            test = True

        self.stdout.write('🔍 INICIANDO DIAGNÓSTICO DEL SISTEMA LMS\n' + '=' * 60)

        # ========== 1. DIAGNÓSTICO ==========
        problemas = []
        advertencias = []
        ok = []

        # 1.1 Verificar modelos y tablas
        self.stdout.write('\n📊 [1] DIAGNOSTICANDO MODELOS Y TABLAS...')
        modelos = ['LinguisticTechnique', 'Curso', 'Leccion', 'Ejercicio', 'Evaluacion', 'ProgresoEstudiante', 'Certificado', 'RespuestaEjercicio']
        for modelo in modelos:
            try:
                model = globals()[modelo]
                if model.objects.exists():
                    count = model.objects.count()
                    ok.append(f'✅ {modelo}: {count} registros')
                else:
                    advertencias.append(f'⚠️ {modelo}: tabla vacía')
            except Exception as e:
                problemas.append(f'❌ {modelo}: {str(e)}')

        # 1.2 Verificar técnicas
        self.stdout.write('\n📚 [2] DIAGNOSTICANDO TÉCNICAS...')
        tecnicas = LinguisticTechnique.objects.all()
        total_tecnicas = tecnicas.count()
        if total_tecnicas == 0:
            problemas.append('❌ No hay técnicas en la base de datos')
        else:
            ok.append(f'✅ Técnicas: {total_tecnicas}')
            sin_categoria = tecnicas.filter(Q(category__isnull=True) | Q(category='')).count()
            if sin_categoria > 0:
                advertencias.append(f'⚠️ {sin_categoria} técnicas sin categoría')
            sin_teoria = tecnicas.filter(theory='').count()
            sin_ejercicio = tecnicas.filter(exercise_text='').count()
            if sin_teoria > 0:
                advertencias.append(f'⚠️ {sin_teoria} técnicas sin teoría')
            if sin_ejercicio > 0:
                advertencias.append(f'⚠️ {sin_ejercicio} técnicas sin ejercicio')

        # 1.3 Verificar cursos
        self.stdout.write('\n🎓 [3] DIAGNOSTICANDO CURSOS...')
        cursos = Curso.objects.all()
        total_cursos = cursos.count()
        if total_cursos == 0:
            advertencias.append('⚠️ No hay cursos creados')
        else:
            ok.append(f'✅ Cursos: {total_cursos}')
            cursos_sin_lecciones = cursos.annotate(num_lecciones=Count('lecciones')).filter(num_lecciones=0)
            if cursos_sin_lecciones.exists():
                advertencias.append(f'⚠️ {cursos_sin_lecciones.count()} cursos sin lecciones')

        # 1.4 Verificar lecciones
        self.stdout.write('\n📖 [4] DIAGNOSTICANDO LECCIONES...')
        lecciones = Leccion.objects.all()
        total_lecciones = lecciones.count()
        if total_lecciones == 0:
            advertencias.append('⚠️ No hay lecciones creadas')
        else:
            ok.append(f'✅ Lecciones: {total_lecciones}')
            lecciones_sin_ejercicios = lecciones.annotate(num_ejercicios=Count('ejercicios')).filter(num_ejercicios=0)
            if lecciones_sin_ejercicios.exists():
                advertencias.append(f'⚠️ {lecciones_sin_ejercicios.count()} lecciones sin ejercicios')

        # 1.5 Verificar ejercicios
        self.stdout.write('\n📝 [5] DIAGNOSTICANDO EJERCICIOS...')
        ejercicios = Ejercicio.objects.all()
        total_ejercicios = ejercicios.count()
        if total_ejercicios == 0:
            advertencias.append('⚠️ No hay ejercicios creados')
        else:
            ok.append(f'✅ Ejercicios: {total_ejercicios}')
            sin_respuesta = ejercicios.filter(respuesta_correcta='').count()
            if sin_respuesta > 0:
                advertencias.append(f'⚠️ {sin_respuesta} ejercicios sin respuesta correcta')

        # 1.6 Verificar evaluaciones
        self.stdout.write('\n📊 [6] DIAGNOSTICANDO EVALUACIONES...')
        evaluaciones = Evaluacion.objects.all()
        total_evaluaciones = evaluaciones.count()
        if total_evaluaciones == 0:
            advertencias.append('⚠️ No hay evaluaciones creadas')
        else:
            ok.append(f'✅ Evaluaciones: {total_evaluaciones}')
            total_preguntas = sum(len(e.preguntas) for e in evaluaciones)
            ok.append(f'   Total preguntas: {total_preguntas}')

        # 1.7 Verificar usuarios
        self.stdout.write('\n👤 [7] DIAGNOSTICANDO USUARIOS...')
        total_usuarios = User.objects.count()
        if total_usuarios == 0:
            advertencias.append('⚠️ No hay usuarios creados')
        else:
            ok.append(f'✅ Usuarios: {total_usuarios}')
            admins = User.objects.filter(is_superuser=True).count()
            staff = User.objects.filter(is_staff=True, is_superuser=False).count()
            estudiantes = User.objects.filter(is_staff=False, is_superuser=False).count()
            ok.append(f'   Admins: {admins}, Profesores: {staff}, Estudiantes: {estudiantes}')

        # 1.8 Verificar progreso y certificados
        self.stdout.write('\n📈 [8] DIAGNOSTICANDO PROGRESO Y CERTIFICADOS...')
        progresos = ProgresoEstudiante.objects.count()
        certificados = Certificado.objects.count()
        respuestas = RespuestaEjercicio.objects.count()
        ok.append(f'✅ Progresos: {progresos}')
        ok.append(f'✅ Certificados: {certificados}')
        ok.append(f'✅ Respuestas: {respuestas}')

        # 1.9 Resumen de diagnóstico
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('📋 RESUMEN DEL DIAGNÓSTICO')
        self.stdout.write('-' * 60)
        for line in ok:
            self.stdout.write(self.style.SUCCESS(line))
        for line in advertencias:
            self.stdout.write(self.style.WARNING(line))
        for line in problemas:
            self.stdout.write(self.style.ERROR(line))
        self.stdout.write('=' * 60)

        # ========== 2. CORRECCIÓN ==========
        if fix:
            self.stdout.write('\n🔧 [FIX] CORRIGIENDO PROBLEMAS DETECTADOS...')
            self._corregir_problemas(problemas, advertencias)

        # ========== 3. COMPLETADO ==========
        if generate:
            self.stdout.write('\n🚀 [GENERATE] COMPLETANDO DATOS FALTANTES...')
            self._completar_datos()

        # ========== 4. PRUEBAS ==========
        if test:
            self.stdout.write('\n🧪 [TEST] EJECUTANDO PRUEBAS DE INTEGRACIÓN...')
            self._ejecutar_pruebas()

        # ========== 5. RESUMEN FINAL ==========
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ DIAGNÓSTICO Y REPARACIÓN COMPLETADOS'))
        self.stdout.write('=' * 60)

    # ==================== FUNCIONES DE CORRECCIÓN ====================

    def _corregir_problemas(self, problemas, advertencias):
        """Corrige problemas comunes"""
        # 1. Corregir técnicas sin categoría
        sin_cat = LinguisticTechnique.objects.filter(Q(category__isnull=True) | Q(category=''))
        if sin_cat.exists():
            self.stdout.write('🔄 Asignando categoría "General" a técnicas sin categoría...')
            sin_cat.update(category='General')

        # 2. Corregir relaciones rotas (lecciones sin curso)
        lecciones_sin_curso = Leccion.objects.filter(curso__isnull=True)
        if lecciones_sin_curso.exists():
            self.stdout.write('🔄 Asignando curso por defecto a lecciones huérfanas...')
            curso_default, _ = Curso.objects.get_or_create(titulo='Curso General')
            lecciones_sin_curso.update(curso=curso_default)

        # 3. Corregir ejercicios sin respuesta correcta
        ejercicios_sin_respuesta = Ejercicio.objects.filter(respuesta_correcta='')
        if ejercicios_sin_respuesta.exists():
            self.stdout.write('🔄 Asignando respuesta por defecto a ejercicios sin respuesta...')
            for ej in ejercicios_sin_respuesta:
                ej.respuesta_correcta = 'Revisa la teoría para encontrar la respuesta.'
                ej.save()

        # 4. Crear superusuario si no existe
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('🔄 Creando superusuario admin...')
            User.objects.create_superuser('admin', 'admin@linguakit.com', 'admin123')

        self.stdout.write(self.style.SUCCESS('✅ Correcciones aplicadas'))

    # ==================== FUNCIONES DE COMPLETADO ====================

    def _completar_datos(self):
        """Completa datos faltantes (cursos, lecciones, ejercicios, evaluaciones)"""
        tecnicas = list(LinguisticTechnique.objects.all())
        if not tecnicas:
            self.stdout.write(self.style.ERROR('❌ No hay técnicas. No se puede generar contenido.'))
            return

        # 1. Crear cursos si no existen
        if Curso.objects.count() == 0:
            self.stdout.write('🔄 Generando cursos automáticamente...')
            from django.core.management import call_command
            call_command('generar_contenido_total', num_cursos=10, ejercicios_por_leccion=50)

        # 2. Generar 100 ejercicios por lección si faltan
        lecciones = Leccion.objects.filter(ejercicios__isnull=True)
        if lecciones.exists():
            self.stdout.write('🔄 Generando ejercicios para lecciones sin ejercicios...')
            from django.core.management import call_command
            call_command('rellenar_100_ejercicios', min_ejercicios=100)

        # 3. Generar evaluaciones si no existen
        cursos_sin_eval = [c for c in Curso.objects.all() if not hasattr(c, 'evaluaciones') or c.evaluaciones.count() == 0]
        if cursos_sin_eval:
            self.stdout.write(f'🔄 Generando evaluaciones para {len(cursos_sin_eval)} cursos...')
            from django.core.management import call_command
            call_command('generar_evaluaciones_masivas', num_preguntas=500)

        self.stdout.write(self.style.SUCCESS('✅ Datos completados'))

    # ==================== FUNCIONES DE PRUEBAS ====================

    def _ejecutar_pruebas(self):
        """Ejecuta pruebas de integración simulando navegación"""
        from django.test import Client
        from django.urls import reverse, NoReverseMatch
        client = Client()
        resultados = []

        # Obtener IDs reales de la base de datos
        curso_id = Curso.objects.first().id if Curso.objects.exists() else 1
        leccion_id = Leccion.objects.first().id if Leccion.objects.exists() else 1

        # Definir rutas con nombre y argumentos
        rutas = [
            ('content:home', []),
            ('content:index', []),
            ('content:listar_cursos', []),
            ('content:detalle_curso', [curso_id]),
            ('content:detalle_leccion', [leccion_id]),
            ('content:buscar', []),
        ]

        for ruta, args in rutas:
            nombre = ruta
            try:
                url = reverse(ruta, args=args) if args else reverse(ruta)
                response = client.get(url)
                if response.status_code == 200:
                    resultados.append(f'✅ {nombre} ({url}) - OK')
                elif response.status_code == 302:
                    resultados.append(f'⚠️ {nombre} ({url}) - Redirección (login)')
                else:
                    resultados.append(f'❌ {nombre} ({url}) - Error {response.status_code}')
            except NoReverseMatch:
                resultados.append(f'❌ {nombre} - No existe en urls.py')
            except Exception as e:
                resultados.append(f'❌ {nombre} - Excepción: {str(e)}')

        # Probar login con credenciales reales
        try:
            from django.contrib.auth import authenticate
            user = authenticate(username='admin', password='admin123')
            if user:
                resultados.append('✅ Login - Credenciales correctas')
            else:
                # Intentar crear admin si no existe
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser('admin', 'admin@linguakit.com', 'admin123')
                    resultados.append('✅ Login - Superusuario admin creado')
                else:
                    resultados.append('⚠️ Login - Credenciales incorrectas (verifica contraseña)')
        except Exception as e:
            resultados.append(f'❌ Login - Excepción: {str(e)}')

        # Mostrar resultados
        self.stdout.write('\n📋 RESULTADOS DE PRUEBAS')
        self.stdout.write('-' * 60)
        for r in resultados:
            if '✅' in r:
                self.stdout.write(self.style.SUCCESS(r))
            elif '❌' in r:
                self.stdout.write(self.style.ERROR(r))
            else:
                self.stdout.write(self.style.WARNING(r))
        self.stdout.write('-' * 60)
