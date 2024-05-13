from facultad.models import Facultad
from .serializers import FacultadSerializers
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def facultad_list(request):
    if request.method == "GET":
        facultades = Facultad.objects.all()
        serializer = FacultadSerializers(facultades, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        serializer =  FacultadSerializers(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def facultad_detail(request, pk):
    try:
        facultad = Facultad.objects.get(id=pk)
    except Facultad.DoesNotExist:
        return Response({"Error":"No existe una facultad con ese ID. "}, status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = FacultadSerializers(facultad)
        return Response(serializer.data, status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = FacultadSerializers(facultad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        facultad.delete()
        return Response(status.HTTP_200_OK)
