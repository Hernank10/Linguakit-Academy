from django.db import models
from apps.core.models import Programa

class SecuenciaDidactica(models.Model):
    programa = models.OneToOneField(Programa, on_delete=models.CASCADE, related_name='secuencia')
    objetivo_general = models.TextField()
    introduccion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'contenidos'
        verbose_name = "Secuencia Didáctica"
