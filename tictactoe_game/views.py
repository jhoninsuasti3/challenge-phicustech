# accounts/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
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
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            # Asociar el token al jugador correspondiente
            jugador = Jugador.objects.get(user=user)
            jugador.token = token
            jugador.save()
            #Response({'user': user}, status=status.HTTP_200_OK)
            # CAMBIO: Devuelve un objeto Response con el status code HTTP_302 y la URL de la plantilla home.html en la cabecera Location.
            return redirect('home')  # Redirige a la vista de inicio de partida
        return render(request, 'login.html', {'error': 'Credenciales inválidas'})
        #return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder
    def post(self, request, *args, **kwargs):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomUserListAPIView(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Home del proycto


def home_view(request):
    return render(request, 'home.html')

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_actual'] = self.request.user
        print("-----------")
        print(context)
        return context


"""
class HomePageView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        usuario_actual = request.user  # Obtiene el usuario autenticado
        print("*****************"*10)
        print(usuario_actual)
        print("*****************"*10)
        jugadores_disponibles = Jugador.objects.exclude(user=usuario_actual)
        from pprint import pprint
        return render(request, 'home.html', {'jugadores_disponibles': jugadores_disponibles, 'usuario_actual': usuario_actual})


"""
# APIS DE LOGICA DE JUEGO

class IniciarPartidaAPIView(APIView):
    def post(self, request, *args, **kwargs):
        usuario_actual = request.user
        serializer = IniciarPartidaSerializer(data=request.data)

        if serializer.is_valid():
            jugador_2_username = serializer.validated_data['jugador_2']

            try:
                jugador_1 = Jugador.objects.get(user=usuario_actual)
                jugador_2 = Jugador.objects.get(user__username=jugador_2_username)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugadores no encontrados.'}, status=status.HTTP_404_NOT_FOUND)

            partida_existente = Partida.objects.filter(
                partida_iniciada=True,
                jugador_1=jugador_1
            ) | Partida.objects.filter(
                partida_iniciada=True,
                jugador_2=jugador_1
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



