# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser, Jugador

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Crear el objeto Jugador relacionado con el CustomUser (sin asignar simbolo)
        Jugador.objects.create(user=user)

        return user


class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = '__all__'

    def validate_simbolo(self, value):
        if value not in ['X', 'O']:
            raise serializers.ValidationError("El símbolo debe ser 'X' o 'O'.")
        return value
        

class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


#Logica del Juego

class IniciarPartidaSerializer(serializers.Serializer):
    jugador_2 = serializers.CharField()