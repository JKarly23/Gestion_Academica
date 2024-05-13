from rest_framework import serializers
from estudiantes.models import Estudiante
from user_app.api.serializers import AccountSerializers

class EstudianteSerializers(serializers.ModelSerializer):
    user = AccountSerializers()
    class Meta:
        model = Estudiante
        fields = "__all__"
        
