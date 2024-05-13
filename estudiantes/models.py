from django.db import models
from grupos.models import Grupo
from facultad.models import Facultad
from user_app.models import Account



# Create your models here.


class Estudiante(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="estudiante")
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="grupos", blank=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="facultad_estudiantes")
    ano_docente = models.IntegerField()
    avg_calificacion = models.FloatField(blank=True, null= True)
    

    def __str__(self) -> str:
        return f"{self.user.first_name} + {self.user.last_name}"
    
