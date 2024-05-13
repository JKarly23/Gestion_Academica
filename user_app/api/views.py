import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from asignatura.models import Asignatura
from estudiantes.models import Estudiante
from facultad.models import Facultad
from grupos.models import Grupo
from user_app.models import Account
from .serializers import AccountSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from .send_mail import send_username
from django.contrib.auth import authenticate
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from profesor.models import Profesor

@api_view(['POST'])
@permission_classes([IsAdminUser])
def registrar(request):

    if request.method == "POST":
        serializer = AccountSerializers(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            print(request.data)
            data['message'] = "El registro fue exitoso"
            data.update(serializer.data)
            data['facultad'] = request.data['facultad']
            facultad = Facultad.objects.get(name=data['facultad'])
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            send_username(data['username'],request.data.get('password'),data['email'])

            if data['role'] == 'profesor':
                data['asignatura'] = request.data.get('asignatura')
                asignatura = Asignatura.objects.get(name=data['asignatura'])
                # Crear el profesor
                
                profesores = Profesor.objects.filter(facultad=facultad,asignatura=asignatura)
                if profesores:
                    return Response({"Asignatura":"Ya existe un profesor para esta asignatura en esta facultad"})
                profesor = Profesor.objects.create(
                    user=account, facultad=facultad)
                profesor.asignatura.add(asignatura)
                
                # Actualizar la cantidad de profesor de la facultad

                facultad_id = facultad.id
                cantidad_profesores = Profesor.objects.filter(
                    facultad=facultad_id).count()
                Facultad.objects.filter(id=facultad_id).update(
                    cantidad_profesores=cantidad_profesores)

            elif data['role'] == 'estudiante':
                data['ano_docente'] = request.data.get('ano_docente')

                # Elegir un grupo aleatorio entre los 4 existan
                grupo_base = data['ano_docente'] * 100
                lista_grupo = [str(grupo_base + i) for i in range(1, 5)]
                while True:
                    numero_grupo = random.choice(lista_grupo)
                    try:
                        grupo = Grupo.objects.get(numero_grupo=numero_grupo)
                        data['grupo'] = grupo.numero_grupo
                        break
                    except Grupo.DoesNotExist:
                        continue

                # Crear el estudiante
                Estudiante.objects.create(
                    user=account, grupo=grupo, facultad=facultad, ano_docente=data['ano_docente'])

                # Actualizar la cantidad de estudiantes en el grupo
                cantidad_estudiantes = Estudiante.objects.filter(
                    grupo=grupo.id).count()
                Grupo.objects.filter(id=grupo.id).update(
                    cantidad_estudiantes=cantidad_estudiantes)

                # Actualizar la cantidad de estudiantes en la facultad
                facultad_id = facultad.id
                cantidad_estudiantes = Estudiante.objects.filter(
                    facultad=facultad_id).count()
                Facultad.objects.filter(id=facultad_id).update(
                    cantidad_estudiantes=cantidad_estudiantes)
        else:
            data = serializer.errors
        

        return Response(data)



@api_view(["POST",])
def loggin(request):
    if request.method == "POST":
        data = {}
        username = request.data.get('username')
        password = request.data.get('password')

        account = authenticate(username=username, password=password)

        if account is not None:
            data['message']="Autenticacion exitosa"
            data['first_name']=account.first_name
            data['last_name']=account.last_name
            data['email']=account.email
            data['username']=username
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data)
        else:
            return Response({"Error":"Credenciales Incorrectas"},status.HTTP_500_INTERNAL_SERVER_ERROR)
        

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def cerrar_sesion(request):
    try:
        # Obtener el token de refresco del cuerpo de la solicitud o de donde sea que esté almacenado
        token = request.data.get('refresh')
        print(str(token))

        if not token:
            return Response({"error": "No se proporcionó el token de refresco"}, status=status.HTTP_400_BAD_REQUEST)

        # Invalidar el token de refresco para prevenir la obtención de nuevos tokens de acceso
        RefreshToken(token).blacklist()

        return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET",])
@permission_classes([IsAdminUser])
def myprofile(request):
    print(request)
    if request.user.is_authenticated:
        user = request.user
        serializer = AccountSerializers(user)
        return Response(serializer.data)
    else:
        return Response({"user":"User not in seccion"})


class AccountListAv(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request):
        users = Account.objects.all()
        serializer = AccountSerializers(users, many=True)
        return Response(serializer.data)
    
class AccountDetail(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        user = Account.objects.get(id=pk)
        serializer = AccountSerializers(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = Account.objects.get(id=pk)
        serializer = AccountSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        user = Account.objects.get(id=pk)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    

