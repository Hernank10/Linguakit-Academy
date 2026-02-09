from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.cursos.models import Inscripcion

@login_required
def perfil(request):
    mis_inscripciones = Inscripcion.objects.filter(usuario=request.user)
    return render(request, 'usuarios/perfil.html', {'inscripciones': mis_inscripciones})
