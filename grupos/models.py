from django.db import models
from facultad.models import Facultad

# Create your models here.

class Grupo(models.Model):
    numero_grupo = models.CharField(max_length=50)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    cantidad_estudiantes = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.numero_grupo} " 
    
