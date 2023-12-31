# accounts/urls.py

from django.urls import path
from .views import  RegisterUserAPIView, UserLoginAPIView, UserLogoutAPIView, CustomUserListAPIView, IniciarPartidaAPIView, RealizarMovimientoAPIView, HomePageView, UserDetailsView, GatewayAPIS, MostrarTablero
from .views import register_success_view

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('users/', CustomUserListAPIView.as_view(), name='users'),

    path('register/success/', register_success_view, name='register_success'),  # Configura una URL para el éxito
    # aPIS DEL JUEGO
    path('api/user_details/', UserDetailsView.as_view(), name='user-details'),
    #path('user-details/', UserDetailsView.as_view(), name='user-details'),
    #path('home/', home_view, name='home'),
    #path('homea/', HomePageView.as_view(), name='homea'),
    #path('home/', Home.as_view(), name='home'),
    path('home/<str:token>', HomePageView.as_view(), name='home'),
    path('game/<int:partida_id>/', MostrarTablero.as_view(), name='game'),
    path('api/iniciar_partida/', IniciarPartidaAPIView.as_view(), name='iniciar_partida'),  # Modifica esta línea # Nueva vista
    path('realizar_movimiento/<int:partida_id>/', RealizarMovimientoAPIView.as_view(), name='realizar_movimiento'),
    path('gateway/', GatewayAPIS.as_view(), name='gateway'),

    path('documentation/', include_docs_urls(title='TicTacToe Game')),

]