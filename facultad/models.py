from django.db import models

# Create your models here.

class Facultad(models.Model):   
    name = models.CharField(max_length=50)
    cantidad_grupos = models.IntegerField(blank=True, null=True)
    cantidad_estudiantes = models.IntegerField(blank=True, null=True)
    cantidad_profesores = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name