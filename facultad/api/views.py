from facultad.models import Facultad
from .serializers import FacultadSerializers
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthAdminOrReadOnly
from rest_framework.views import APIView

class FacultadListAV(APIView):
    permission_classes = [IsAuthAdminOrReadOnly]
    def get(self, request):
        facultades = Facultad.objects.all()
        serializer = FacultadSerializers(facultades, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self,request):
        serializer =  FacultadSerializers(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class FacultadDetailAV(APIView):
    permission_classes = [IsAuthAdminOrReadOnly]
    def get(self,request,pk):
        try:
            facultad = Facultad.objects.get(id=pk)
            serializer = FacultadSerializers(facultad)
            return Response(serializer.data, status.HTTP_200_OK)
        except Facultad.DoesNotExist:
            return Response({"Error":"No existe una facultad con ese ID. "}, status.HTTP_404_NOT_FOUND)
    

    
    def put(self,request,pk):
        try:
            facultad = Facultad.objects.get(id=pk)
            serializer = FacultadSerializers(facultad, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Facultad.DoesNotExist:
            return Response({"Error":"No existe una facultad con ese ID. "}, status.HTTP_404_NOT_FOUND)
        
 
    def delete(self,request,pk):
        try:
            facultad = Facultad.objects.get(id=pk)
            facultad.delete()
            return Response(status.HTTP_200_OK)
        except Facultad.DoesNotExist:
            return Response({"Error":"No existe una facultad con ese ID. "}, status.HTTP_404_NOT_FOUND)

            
