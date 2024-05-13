from grupos.models import Grupo
from rest_framework.views import APIView
from .serializers import GruposSerializers
from rest_framework.response import Response
from rest_framework import status
from facultad.models import Facultad


class GruposListAV(APIView):

    def get(self, request):
        grupos = Grupo.objects.all()
        serializer = GruposSerializers(grupos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = GruposSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            facultad_id = serializer.validated_data['facultad']
            cantidad_grupos = Grupo.objects.filter(facultad_id=facultad_id).count()
            Facultad.objects.filter(id=facultad_id.id).update(cantidad_grupos=cantidad_grupos)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class GrupoDetailAV(APIView):

    def get(self, request, pk):
        try:
            grupo = Grupo.objects.get(id=pk)
            serializer = GruposSerializers(grupo)
            return Response(serializer.data)
        except Grupo.DoesNotExist:
            return Response({"Error": "No existe un grupo con ese ID."}, status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            grupo = Grupo.objects.get(id=pk)
            serializer = GruposSerializers(grupo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Grupo.DoesNotExist:
            return Response({"Error": "No existe un grupo con ese ID."}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            grupo = Grupo.objects.get(id=pk)
            grupo.delete()
            return Response(status.HTTP_200_OK)
        except Grupo.DoesNotExist:
            return Response({"Error": "No existe un grupo con ese ID."}, status.HTTP_404_NOT_FOUND)
