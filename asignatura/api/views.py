from rest_framework.viewsets import ModelViewSet
from asignatura.models import Asignatura, ComentarioAsignatura, Nota
from profesor.models import Profesor
from .serializers import AsignaturaSerializers, ComentarioSerializers, NotaSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from estudiantes.models import Estudiante
from estudiantes.api.permissions import IsEstudianteAuth
from profesor.api.permissions import IsProfesorAuth
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from django.db.models import Avg



class AsignaturasVS(APIView):
    
    def get(self, request):
        asignaturas = Asignatura.objects.all()
        serializer = AsignaturaSerializers(asignaturas, many=True)
        return Response(serializer.data,status=200)
    
    @permission_classes([IsAdminUser])
    def post(self, request):
        serializer = AsignaturaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    

class AsignaturasDetailAV(APIView):

    def get(self, request, pk):
        asignatura = Asignatura.objects.get(id=pk)
        serializer = AsignaturaSerializers(asignatura)
        return Response(serializer.data, status=200)

    @permission_classes([IsAdminUser])
    def put(self, request, pk):
        asignatura = Asignatura.objects.get(id=pk)
        serializer = AsignaturaSerializers(asignatura,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.error, status=400)

    @permission_classes([IsAdminUser])    
    def delete(self, request, pk):
        asignatura = Asignatura.objects.get(id=pk)
        asignatura.delete()
        return Response(status=200)



class ComentarioListAV(APIView):

    def get(self, request, pk):
        try:
            comentarios = ComentarioAsignatura.objects.all()
            serializers = ComentarioSerializers(comentarios, many=True)
            return Response(serializers.data, status.HTTP_200_OK)
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)
    @permission_classes([IsEstudianteAuth])
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
    
    @permission_classes([IsEstudianteAuth])
    def put(self, request, pk):

        try:
            comentario = ComentarioAsignatura.objects.get(id=pk)
            if comentario.estudiante == request.user:
                serializers = ComentarioSerializers(comentario, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data, status.HTTP_200_OK)
                else:
                    return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Estudiante":"No puede modificar este comentario"})
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)
    @permission_classes([IsEstudianteAuth])    
    def delete(self, request, pk):
        try:
            comentario = ComentarioAsignatura.objects.get(id=pk)
            if comentario.estudiante == request.user:
                comentario.delete()
                return Response(status.HTTP_202_ACCEPTED)
            else:
                return Response({"Estudiante":"No puede eliminar este comentario"})
        except ComentarioAsignatura.DoesNotExist:
            return Response({"Error": "No existe un comentario con ese ID."}, status.HTTP_404_NOT_FOUND)


class NotasListAV(APIView):

    def get(self, request, pk):
        try:
            notas = Nota.objects.filter(estudiante=pk)
            serializers = NotaSerializers(notas, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Nota.DoesNotExist:
            return Response({"Error": "No existe una nota con ese ID."}, status=status.HTTP_404_NOT_FOUND)


    #Hacer validaciones para cuando un profesor inserte una nota a un estudiante este reciva la asignatura
    @permission_classes([IsProfesorAuth])
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
    @permission_classes([IsProfesorAuth])
    def put(self, request, pk):
        try:
            queryset = Nota.objects.get(id=pk)
            if queryset.profesor == request.user:
                serializers = NotaSerializers(queryset, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data, status.HTTP_200_OK)
                else:
                    return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Notas":"No tiene permiso para modificar esta nota"})
        except Nota.DoesNotExist:
            return Response({"Error": {"No existe una nota con ese ID. "}})

    @permission_classes([IsProfesorAuth])
    def delete(self, request, pk):
        try:
            queryset = Nota.objects.get(id=pk)
            if queryset.profesor == request.user:
                queryset.delete()
                return Response(status.HTTP_202_ACCEPTED)
            else:
                 return Response({"Notas":"No tiene permiso para eliminar esta nota"})
        except Nota.DoesNotExist:
            return Response({"Error": {"No existe una nota con ese ID. "}})
