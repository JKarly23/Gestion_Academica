from rest_framework import serializers
from facultad.models import Facultad

class FacultadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = "__all__"


    def create(self, validated_data):
        return Facultad.objects.create(**validated_data)


    def update(self, instace, validated_data):
        instace.name = validated_data.get('name', instace.name)
        instace.save()
        return instace