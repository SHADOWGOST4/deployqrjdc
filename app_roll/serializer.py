from rest_framework import serializers
from .models import Mesa, MesaHasUsuario, Personaje, PjConocido, Atributo, Equipamiento, Habilidad
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'email', 'password']

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'

class MesaHasUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesaHasUsuario
        fields = '__all__'

class PersonajeSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Personaje
        fields = '__all__'

class PjConocidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PjConocido
        fields = '__all__'

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'

class EquipamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamiento
        fields = '__all__'

class HabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidad
        fields = '__all__'
    
    
    
class MesaCreateSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(write_only=True)  # Campo para recibir el ID del usuario desde el frontend

    class Meta:
        model = Mesa
        fields = ['nombre','tematica', 'descripcion' , 'user_id']  # Incluye el campo user_id
        
    def create(self, validated_data):
        # Extrae el user_id del validated_data
        user_id = validated_data.pop('user_id')
    
        # Crear la mesa
        mesa = Mesa.objects.create(**validated_data)
    
        # Obtén el usuario a partir del user_id
        user = User.objects.get(id=user_id)

        # Crear la relación MesaHasUsuario para asignar el rol de Gamemaster
        MesaHasUsuario.objects.create(mesa=mesa, usuario=user, rol='GAMEMASTER')

        return mesa


    