import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils import timezone

# Importar modelo de usuario personalizado
from apps.usuarios.models import Usuario

try:
    from apps.cursos.models import Curso, Inscripcion
    CURSOS_EXISTEN = True
except ImportError:
    CURSOS_EXISTEN = False

class Command(BaseCommand):
    help = 'Crea usuarios con roles (admin, profesor, estudiante) usando modelo personalizado'

    def add_arguments(self, parser):
        parser.add_argument('--num-estudiantes', type=int, default=10)
        parser.add_argument('--num-profesores', type=int, default=3)
        parser.add_argument('--password', type=str, default='password123')
        parser.add_argument('--clear', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        num_estudiantes = options['num_estudiantes']
        num_profesores = options['num_profesores']
        password = options['password']
        clear = options['clear']

        if clear:
            Usuario.objects.filter(is_superuser=False).delete()
            self.stdout.write('🗑️ Usuarios eliminados')

        self._crear_grupos()
        self._crear_admin(password)
        profesores = self._crear_profesores(num_profesores, password)
        estudiantes = self._crear_estudiantes(num_estudiantes, password)

        self._mostrar_resumen()

    def _crear_grupos(self):
        grupos = {
            'Profesores': ['add_curso', 'change_curso', 'delete_curso', 'view_curso',
                           'add_leccion', 'change_leccion', 'view_leccion',
                           'add_ejercicio', 'change_ejercicio', 'view_ejercicio'],
            'Estudiantes': ['view_curso', 'view_leccion', 'view_ejercicio']
        }
        for nombre, permisos in grupos.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            for codename in permisos:
                perm = Permission.objects.filter(codename=codename).first()
                if perm:
                    grupo.permissions.add(perm)

    def _crear_admin(self, password):
        if not Usuario.objects.filter(is_superuser=True).exists():
            Usuario.objects.create_superuser('admin', 'admin@linguakit.com', password)
            self.stdout.write('✅ Admin creado')

    def _crear_profesores(self, cantidad, password):
        profesores = []
        for i in range(1, cantidad + 1):
            username = f'profesor{i}'
            if not Usuario.objects.filter(username=username).exists():
                user = Usuario.objects.create_user(username, f'{username}@linguakit.com', password)
                user.is_staff = True
                user.save()
                user.groups.add(Group.objects.get(name='Profesores'))
                profesores.append(user)
        return profesores

    def _crear_estudiantes(self, cantidad, password):
        estudiantes = []
        for i in range(1, cantidad + 1):
            username = f'estudiante{i}'
            if not Usuario.objects.filter(username=username).exists():
                user = Usuario.objects.create_user(username, f'{username}@linguakit.com', password)
                user.groups.add(Group.objects.get(name='Estudiantes'))
                estudiantes.append(user)
        return estudiantes

    def _mostrar_resumen(self):
        total = Usuario.objects.count()
        admins = Usuario.objects.filter(is_superuser=True).count()
        staff = Usuario.objects.filter(is_staff=True, is_superuser=False).count()
        estudiantes = Usuario.objects.filter(is_staff=False, is_superuser=False).count()
        self.stdout.write(f'\n📊 Total: {total} | Admins: {admins} | Profesores: {staff} | Estudiantes: {estudiantes}')
        self.stdout.write('🔑 password123 para todos los usuarios')
