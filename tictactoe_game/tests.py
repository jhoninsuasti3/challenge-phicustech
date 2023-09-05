from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from tictactoe_game.views import HomePageView

class UserLoginAPIViewTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.username = "testuser"
        self.password = "testpassword"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password
        )
        self.token = Token.objects.create(user=self.user)

    def test_login_view_get(self):
        # Prueba la vista de inicio de sesión con un método GET
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid_credentials(self):
        # Prueba la vista de inicio de sesión con credenciales válidas
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Debería redirigir al usuario a 'home'
        self.assertEqual(response.url, reverse('home', kwargs={'token': self.token.key}))

    def test_login_view_post_invalid_credentials(self):
        # Prueba la vista de inicio de sesión con credenciales inválidas
        response = self.client.post(reverse('login'), {
            'username': 'usuario_invalido',
            'password': 'contraseña_invalida'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('error', response.context)  # Debería haber un mensaje de error en el contexto

    def tearDown(self):
        # Limpia los objetos creados durante las pruebas
        self.user.delete()
        self.token.delete()



class HomePageViewTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba y un token
        self.username = "testuser"
        self.password = "testpassword"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password
        )
        self.token = Token.objects.create(user=self.user)

        # Crear una instancia de RequestFactory
        self.factory = RequestFactory()

    def test_home_page_view_authenticated(self):
        # Prueba la vista de inicio de sesión cuando el usuario está autenticado
        request = self.factory.get(reverse('home'))
        request.user = self.user

        response = HomePageView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('token', response.context_data)
        self.assertIn('usuario_actual', response.context_data)

    def test_home_page_view_unauthenticated(self):
        # Prueba la vista de inicio de sesión cuando el usuario no está autenticado
        request = self.factory.get(reverse('home'))

        response = HomePageView.as_view()(request)

        self.assertEqual(response.status_code, 302)  # Debería redirigir al usuario a la página de inicio de sesión

    def tearDown(self):
        # Limpia los objetos creados durante las pruebas
        self.user.delete()
        self.token.delete()