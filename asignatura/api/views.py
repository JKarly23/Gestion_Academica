from rest_framework.viewsets import ModelViewSet
from asignatura.models import Asignatura, ComentarioAsignatura, Nota
from profesor.models import Profesor
from .serializers import AsignaturaSerializers, ComentarioSerializers, NotaSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from estudiantes.models import Estudiante
#from estudiantes.api.permissions import PermissionsOfStudents
#from profesor.api.permissions import PermissionsOfProfessor



class AsignaturasVS(ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializers
    #permission_classes = [PermissionsOfProfessor,PermissionsOfStudents]

    def perform_create(self, serializer):
        name_subject = serializer.validated_data.get('name')
        id_profesor = serializer.validated_data.get('profesor')
        query = Asignatura.objects.filter(name=name_subject)
        if query.exists():
             return Response(serializer.errors)
        profesor = Profesor.objects.get(id=id_profesor.id)
        if serializer.is_valid():
            serializer.save(name=serializer.validated_data.get('name'), profesor=profesor)
            print(serializer.data)
            return Response(serializer.data, status.HTTP_201_CREATED)

        



class ComentarioListAV(APIView):

    def get(self, request, pk):
        try:
            comentarios = ComentarioAsignatura.objects.all()
            serializers = ComentarioSerializers(comentarios, many=True)
            return Response(serializers.data, status.HTTP_200_OK)
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)
    
    def post(self, request, pk):
        context = {'asignatura_id':pk}
        serializers = ComentarioSerializers(data=request.data, context=context)
        if serializers.is_valid():
            asignatura = serializers.validated_data['asignatura'] 
            estudiante = serializers.validated_data['estudiante']
            query = ComentarioAsignatura.objects.filter(estudiante=estudiante, asignatura=asignatura)
            if query.exists():
                return Response({"Error": "El estudiante ya hizo un comentario de la asignatura"}, status.HTTP_400_BAD_REQUEST)
            serializers.save()
            return Response(serializers.data, status.HTTP_200_OK)
    
class CometarioDetailAV(APIView):

    def get(self, request, pk):
        try:
            comentario = ComentarioAsignatura.objects.get(id=pk)
            seriliazers = ComentarioSerializers(comentario)
            return Response(seriliazers.data, status.HTTP_202_ACCEPTED)
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):

        try:
            comentario = ComentarioAsignatura.objects.get(id=pk)
            serializers = ComentarioSerializers(comentario, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status.HTTP_200_OK)
            else:
                return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            comentario = ComentarioAsignatura.objects.get(id=pk)
            comentario.delete()
            return Response(status.HTTP_202_ACCEPTED)
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

class NotasListAV(APIView):

    def get(self, request, pk):
        try:
            notas = Nota.objects.filter(estudiante=pk)
            serializers = NotaSerializers(notas, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Nota.DoesNotExist:
            return Response({"Error": "No existe una nota con ese ID."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            estudiante_pk = pk
            serializers = NotaSerializers(data=request.data, context={'estudiante_pk': estudiante_pk})
            if serializers.is_valid():
                profesor_pk = serializers.validated_data['profesor']
                asignatura_pk = serializers.validated_data['asignatura']
                query = Nota.objects.filter(profesor=profesor_pk, estudiante=estudiante_pk)
                if query.exists():
                    return Response({"Error": "El profesor ya ha registrado una nota para este estudiante."}, status=status.HTTP_400_BAD_REQUEST)
                query = Nota.objects.filter(asignatura=asignatura_pk, estudiante=estudiante_pk)
                if query.exists():
                    return Response({"Error": "Ya existe una nota para esa asignatura."}, status=status.HTTP_400_BAD_REQUEST)
                
                asignatura = Asignatura.objects.get(id=asignatura_pk.id)
                if profesor_pk != asignatura.profesor:
                    return Response({"Error": "El profesor no es el profesor de esa asignatura."}, status=status.HTTP_400_BAD_REQUEST)
                
                serializers.save()
                
                # Calcular y actualizar el promedio del estudiante
                promedio_estudiante = Nota.objects.filter(estudiante=pk).aggregate(promedio=Avg('nota'))
                estudiante = Estudiante.objects.get(id=pk)
                estudiante.avg_calificacion = promedio_estudiante['promedio']
                estudiante.save()
                
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Nota.DoesNotExist:
            return Response({"Error": "No existe una nota con ese ID."}, status=status.HTTP_404_NOT_FOUND)




class NotasDetailAV(APIView):

    def get(self, request, pk):
        try:
            queryset = Nota.objects.get(id=pk)
            serializers = NotaSerializers(queryset)
            return Response(serializers.data, status.HTTP_200_OK)
        except Nota.DoesNotExist:
            return Response({"Error": {"No existe una nota con ese ID. "}})

    def put(self, request, pk):
        try:
            queryset = Nota.objects.get(id=pk)
            serializers = NotaSerializers(queryset, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status.HTTP_200_OK)
            else:
                return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)
        except Nota.DoesNotExist:
            return Response({"Error": {"No existe una nota con ese ID. "}})

    def delete(self, request, pk):
        try:
            queryset = Nota.objects.get(id=pk)
            queryset.delete()
            return Response(status.HTTP_202_ACCEPTED)
        except Nota.DoesNotExist:
            return Response({"Error": {"No existe una nota con ese ID. "}})
