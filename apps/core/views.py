from django.shortcuts import render, get_object_or_404
from .models import Programa

def home(request):
    programas = Programa.objects.all()
    return render(request, 'core/home.html', {'programas': programas})

def curso_detalle(request, curso_id):
    programa = get_object_or_404(Programa, id=curso_id)
    lecciones = programa.lecciones.all()
    return render(request, 'core/curso_detalle.html', {
        'programa': programa,
        'lecciones': lecciones
    })
