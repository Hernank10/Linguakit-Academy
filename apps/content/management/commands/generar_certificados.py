import hashlib
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import ProgresoEstudiante, Certificado

class Command(BaseCommand):
    help = 'Genera certificados para estudiantes que completaron cursos'

    def add_arguments(self, parser):
        parser.add_argument('--curso-id', type=int, help='ID del curso específico')
        parser.add_argument('--estudiante-id', type=int, help='ID del estudiante específico')
        parser.add_argument('--all', action='store_true', help='Generar para todos los estudiantes')

    @transaction.atomic
    def handle(self, *args, **options):
        curso_id = options.get('curso_id')
        estudiante_id = options.get('estudiante_id')

        progresos = ProgresoEstudiante.objects.filter(completado=True, porcentaje_completado__gte=80.0)
        if curso_id:
            progresos = progresos.filter(curso_id=curso_id)
        if estudiante_id:
            progresos = progresos.filter(estudiante_id=estudiante_id)

        if not progresos:
            self.stdout.write('⚠️ No hay estudiantes que hayan completado cursos con ≥80%.')
            return

        certificados_creados = 0
        for progreso in progresos:
            if Certificado.objects.filter(estudiante=progreso.estudiante, curso=progreso.curso).exists():
                continue
            codigo = hashlib.md5(
                f"{progreso.estudiante.id}{progreso.curso.id}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:12].upper()
            Certificado.objects.create(
                estudiante=progreso.estudiante,
                curso=progreso.curso,
                codigo=codigo,
                puntaje_final=progreso.puntaje_total / max(progreso.ejercicios_completados, 1) * 100
            )
            certificados_creados += 1
            self.stdout.write(f'✅ Certificado para {progreso.estudiante.username} - {progreso.curso.titulo} (Código: {codigo})')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 {certificados_creados} certificados generados'))
