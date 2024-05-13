from rest_framework.response import Response
from profesor.models import Profesor
from.serializers import ProfesorSerializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser




class ProfesorListAV(APIView):

    def get(self, request):
        profesores = Profesor.objects.all()
        serializers = ProfesorSerializers(profesores, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class ProfesorDetailAV(APIView):
    def get(self, request,pk):
        profesor = Profesor.objects.get(id=pk)
        serializer = ProfesorSerializers(profesor)
        return Response(serializer.data)
    
    @permission_classes([IsAdminUser])
    def put(self, request, pk):
        profesor = Profesor.objects.get(id=pk)
        serializer = ProfesorSerializers(profesor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED) 

    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        profesor = Profesor.objects.get(id=pk)
        profesor.delete()
        return Response(status.HTTP_200_OK)
