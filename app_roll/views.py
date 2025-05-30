from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
from django.http import JsonResponse
from .utils import obtener_mesas_gamemaster

from django.contrib.auth.models import User

from .models import  Mesa, MesaHasUsuario, Personaje, PjConocido, Atributo, Equipamiento, Habilidad
from .serializer import UserSerializer, MesaSerializer, MesaHasUsuarioSerializer, PersonajeSerializer, PjConocidoSerializer, AtributoSerializer, EquipamientoSerializer, HabilidadSerializer, MesaCreateSerializer


@api_view(['POST'])
def login(request):
    
    user = get_object_or_404(User, username= request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({"error": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user= user)
    serializer = UserSerializer(instance= user)
    return Response({"Token": token.key, "username": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username= serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'usuario': serializer.data}, status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    
    print(request.user.id)
    serializer = UserSerializer(instance= request.user)
     
    return Response(serializer.data, status=status.HTTP_200_OK)



# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class MesaHasUsuarioViewSet(viewsets.ModelViewSet):
    queryset = MesaHasUsuario.objects.all()
    serializer_class = MesaHasUsuarioSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class PersonajeViewSet(viewsets.ModelViewSet):
    queryset = Personaje.objects.all()
    serializer_class = PersonajeSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class PjConocidoViewSet(viewsets.ModelViewSet):
    queryset = PjConocido.objects.all()
    serializer_class = PjConocidoSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class EquipamientoViewSet(viewsets.ModelViewSet):
    queryset = Equipamiento.objects.all()
    serializer_class = EquipamientoSerializer


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class HabilidadViewSet(viewsets.ModelViewSet):
    queryset = Habilidad.objects.all()
    serializer_class = HabilidadSerializer



def mesas_gamemaster(request, user_id):
    mesas_data = obtener_mesas_gamemaster(user_id)
    return JsonResponse(mesas_data, safe=False)


class MesaCreateView(generics.CreateAPIView):
    queryset = Mesa.objects.all()
    serializer_class = MesaCreateSerializer
    


@api_view(['POST'])
def crear_personaje_basico(request, mesa_id):
    try:
        mesa = Mesa.objects.get(id=mesa_id)

        # Creamos el personaje sin asignar un usuario
        personaje = Personaje.objects.create(
            mesa=mesa, 
            usuario=None,  # No asignamos usuario en este momento
            nombre="", 
            edad=0, 
            altura=0.0, 
            nivel=1, 
            hp_base=100, 
            hp_actuales=100, 
            bloqueo=0, 
            esquivar=0, 
            ataque=0
        )
        
        # Serializamos el personaje recién creado
        serializer = PersonajeSerializer(personaje)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Mesa.DoesNotExist:
        return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
def listar_personajes_mesa(request, mesa_id):
    try:
        # Obtener la mesa
        mesa = Mesa.objects.get(id=mesa_id)

        # Obtener los personajes asociados a esa mesa
        personajes = Personaje.objects.filter(mesa=mesa)

        # Serializar solo el ID de cada personaje
        personajes_data = [{"id": personaje.id, "nombre": personaje.nombre} for personaje in personajes]

        return Response(personajes_data, status=status.HTTP_200_OK)

    except Mesa.DoesNotExist:
        return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)