from estudiantes.models import Estudiante
from .serializers import EstudianteSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes

class EstudiantesListAV(APIView):

    def get(self, request):
        estudiantes = Estudiante.objects.all()
        serializers = EstudianteSerializers(estudiantes, many=True)
        return Response(serializers.data, status.HTTP_200_OK)
    

class EstudiantesDetailAV(APIView):

    def get(self, request, pk):
        try:
            estudiante = Estudiante.objects.get(id=pk)
            serializers = EstudianteSerializers(estudiante)
            return Response(serializers.data, status.HTTP_200_OK)
        except Estudiante.DoesNotExist:
            return Response({"Error": "No existe un estudiante con ese ID."},status.HTTP_404_NOT_FOUND)
        
    @permission_classes([IsAdminUser])
    def put(self, request, pk):
        try:
            estudiante = Estudiante.objects.get(id=pk)
            serializers = EstudianteSerializers(estudiante, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status.HTTP_200_OK)
            else:
                return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)
        except Estudiante.DoesNotExist:
            return Response({"Error": "No existe un estudiante con ese ID."}, status.HTTP_404_NOT_FOUND)
        
    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        try:
            estudiante = Estudiante.objects.get(id=pk)
            estudiante.delete()
            return Response(status.HTTP_200_OK)
        except Estudiante.DoesNotExist:
            return Response({"Error": "No existe un estudiante con ese ID."}, status.HTTP_404_NOT_FOUND)
