from django.db import models

from facultad.models import Facultad
from user_app.models import Account
from asignatura.models import Asignatura


# Create your models here.


class Profesor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profesor")
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="facultad_profesor")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

