from django.db import models
from facultad.models import Facultad
from user_app.models import Account



# Create your models here.

class Asignatura(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    


class Profesor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profesor_user")
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="facultad_profesor")
    asignatura = models.ManyToManyField(Asignatura)
    

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

