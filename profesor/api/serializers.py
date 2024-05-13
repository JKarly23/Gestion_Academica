from rest_framework import serializers

from profesor.models import Profesor

class ProfesorSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profesor
        fields = "__all__"

