from rest_framework import serializers
from asignatura.models import Asignatura,ComentarioAsignatura,Nota
from estudiantes.models import Estudiante
from profesor.models import Profesor

class AsignaturaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ["id","name","profesor"]

class ComentarioSerializers(serializers.ModelSerializer):

    class Meta:
        model = ComentarioAsignatura
        fields = "__all__"



class NotaSerializers(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    asignatura_nombre = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Nota
        fields = ["estudiante", "asignatura", "profesor", "nota", "estudiante_nombre", "asignatura_nombre", "profesor_nombre"]

    def get_estudiante_nombre(self, obj):
        estudiante_id = obj.estudiante.id
        # Aquí debes buscar el estudiante en tu modelo Estudiante utilizando el ID
        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            return estudiante.first_name + " " + estudiante.last_name
        except Estudiante.DoesNotExist:
            return "Estudiante no encontrado"

    def get_asignatura_nombre(self, obj):
        asignatura_id = obj.asignatura.id
        # Aquí debes buscar la asignatura en tu modelo Asignatura utilizando el ID
        try:
            asignatura = Asignatura.objects.get(id=asignatura_id)
            return asignatura.name
        except Asignatura.DoesNotExist:
            return "Asignatura no encontrada"

    def get_profesor_nombre(self, obj):
        profesor_id = obj.profesor.id
        # Aquí debes buscar el profesor en tu modelo Profesor utilizando el ID
        try:
            profesor = Profesor.objects.get(id=profesor_id)
            return profesor.first_name + " " + profesor.last_name
        except Profesor.DoesNotExist:
            return "Profesor no encontrado"

    

