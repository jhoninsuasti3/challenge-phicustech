import requests
# accounts/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer, CustomUserListSerializer, IniciarPartidaSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser, Partida, Jugador

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View

from django.views.generic import UpdateView, ListView, TemplateView, CreateView
from django.urls import reverse

from django.db.models import Q
from rest_framework.decorators import authentication_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import get_authorization_header
from django.http import HttpResponseForbidden

from django.views import generic

#Inicio de manejo de usuarios
class RegisterUserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('register_success')  # Redirige a una página de éxito
        return render(request, 'register.html', {'errors': serializer.errors})

class UserLoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')  # Renderiza el formulario de inicio de sesión
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if '@' in username:
            try:
                autenticado = CustomUser.objects.get(email=username)
                
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            # Asociar el token al usuario correspondiente
            u = CustomUser.objects.get(username=user)
            u.token = token.key
            u.save()
            # Imprime el valor del campo token
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            return redirect('home', token =token)
            #context = {'Token': token}
            #return render(request, 'homea.html', context )
            
           #return Response({'user': user.username, 'token': token.key}, status=status.HTTP_200_OK)
        return render(request, 'login.html', {'error': 'Credenciales inválidas'})
        #return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    authentication_classes = (SessionAuthentication )
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder
    def post(self, request, *args, **kwargs):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# End manejo de usuarios



class CustomUserListAPIView(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Home del proycto
def home_view(request):
    return render(request, 'home.html')

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    #print(" //////////////// ")
    def get(self, request, *args, **kwargs):
        print(" //////////////// ")
        cabeceras = self.request.headers
        token = self.kwargs.get('token') 
        from pprint import pprint
        pprint(cabeceras)
        user = self.request.user
        print("-------------------"*2)
        print(user)
        print("-------------------"*2)
        if user.is_authenticated:
            user_details = {
                'username': user.username,
                'email': user.email,
                # Otros detalles que desees mostrar
            }
            return Response(user_details, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se ha autenticado ningún usuario.'}, status=status.HTTP_401_UNAUTHORIZED)


class HomePageView(View):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    template_name = "home.html"
    def get(self, request, *args, **kwargs):  # Corregir 'kwarg' a 'kwargs'
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)  # Usar 'self.template_name'
    def get_context_data(self, **kwargs):
        context = {}
        users = CustomUser.objects.all()
        token = self.kwargs.get('token') 
        user = CustomUser.objects.filter(token=token).first()
        context['token'] = token
        print(token)
        context['usuario_actual'] = str(user)
        if self.request.user.is_authenticated:
            usuarios_autenticados = CustomUser.objects.filter(is_active=True).values('username', 'email')
            #usuarios_autenticados = CustomUser.objects.filter(is_active=True, jugador__token__isnull=False).values('username', 'email')
        # Filtrar los usuarios que no tienen partidas activas
        jugadores_sin_partida = []
        for user in users:
            if not Partida.objects.filter(Q(jugador_1__user=user) | Q(jugador_2__user=user), fecha_fin__isnull=True).exists():
                jugadores_sin_partida.append(user.username)
        context['jugadores_disponibles'] = jugadores_sin_partida
        jugadores_dispo = context['jugadores_disponibles'] = jugadores_sin_partida
        #context['usuarios_autenticados'] = usuarios_autenticados
        #print(context)
        return context
    
# APIS DE LOGICA DE JUEGO

class GatewayAPIS(View):
    def post(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        usuario_actual_username = self.request.GET.get('usuario_actual')
        print("Espere un momento")
        print("--"*20)
        print(f"Usuario: {usuario_actual_username} Token: {token}")
        print("--"*20)
        self.enviar_solicitud_iniciar_partida(usuario_actual)
        return redirect('home')  # Redirige de nuevo a la página de inicio

    def enviar_solicitud_iniciar_partida(self, usuario_actual):
        try:
            user_token = Token.objects.get(user=usuario_actual).key
        except Token.DoesNotExist:
            user_token = None
        
        if user_token:
            url = 'http://localhost:8000/tictactoe_game/api/iniciar_partida/'
            headers = {
                'Authorization': f'Token {user_token}',
                'Content-Type': 'application/json'
            }
            data = {}  # Datos que necesites enviar en la solicitud
            response = requests.post(url, headers=headers, json=data)
            return response
        else:
            return None  # El usuario no está autenticado o no tiene un token válido


class IniciarPartidaAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        token = request.GET.get('token')  # Obtener el token de los parámetros de la URL
        usuario_actual_username = request.GET.get('usuario_actual')
        print(token)
        serializer = IniciarPartidaSerializer(data=request.data)

        if serializer.is_valid():
            jugador_2_username = serializer.validated_data['jugador_2']

            try:
                jugador_1 = Jugador.objects.get(user=usuario_actual)
                jugador_2 = Jugador.objects.get(user__username=jugador_2_username)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugadores no encontrados.'}, status=status.HTTP_404_NOT_FOUND)

            partida_existente = Partida.objects.filter(
                jugador_1=jugador_1,
                fecha_fin__isnull=True
            ) | Partida.objects.filter(
                jugador_2=jugador_1,
                fecha_fin__isnull=True
            )


            if partida_existente.exists():
                return Response({'error': 'Ya existe una partida iniciada con este jugador.'}, status=status.HTTP_400_BAD_REQUEST)
            # Crear la partida y establecer jugador 1, jugador 2 y turno
            partida = Partida.objects.create(
                jugador_1=jugador_1,
                jugador_2=jugador_2,
                turno=jugador_1,
                partida_iniciada=True
            )
            return Response({'message': 'Partida iniciada exitosamente.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IniciarPartidaView(RetrieveAPIView):
    queryset = Partida.objects.all()
    serializer_class = IniciarPartidaSerializer
    template_name = 'game.html'

class RealizarMovimientoAPIView(APIView):
    def post(self, request, partida_id, *args, **kwargs):
        partida = Partida.objects.get(pk=partida_id)
        jugador = partida.turno

        fila = request.data.get('fila')
        columna = request.data.get('columna')

        # Realizar validaciones y lógica de movimiento
        # ...

        movimiento = Movimiento.objects.create(partida=partida, jugador=jugador, fila=fila, columna=columna)
        movimiento_data = {'fila': fila, 'columna': columna, 'jugador': jugador.simbolo}

        # Notificar a los consumidores sobre el movimiento
        async_to_sync(self.notify_consumers)(partida_id, movimiento_data)

        return Response(movimiento_data, status=status.HTTP_201_CREATED)

    def notify_consumers(self, partida_id, movimiento_data):
        partida_group_name = f"partida_{partida_id}"
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            partida_group_name,
            {
                'type': 'movimiento',
                'movimiento': movimiento_data
            }
        )

    def notify_consumers(self, partida_id, movimiento_data):
        partida_group_name = f"partida_{partida_id}"
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            partida_group_name,
            {
                'type': 'movimiento',
                'movimiento': movimiento_data
            }
        )

def register_success_view(request):
    return render(request, 'register_success.html')


class Obtain_Values_APIS:
    def __init__(self, url, token):
        """
        Initialize the Obtain_Values_APIS class with the given url and token.
        
        Args:
        - url (str): The URL of the API.
        - token (str): The authentication token.
        """
        self.url = url
        self.token = token

    def get_data(self):
        """
        Get data from the API using the provided URL and token.
        
        Returns:
        - dict: The response data from the API.
        """
        headers = {
            "Authorization": f"Token {self.token}"
        }

        response = requests.get(self.url, headers=headers)
        data = response.json()
        return data