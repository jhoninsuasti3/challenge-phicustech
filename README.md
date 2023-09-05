## Challenge phicus - Juego tictactoe

Juego a desarrollar en python en el framework Django y DRF.

El proyecto utiliza formularios basicos, y permite a dos jugadores iniciar una partida, solo si estan registrados y autenticados

* Ojo: En el archivo main.py ya esta desarrollada la logica del juego pero en python utilizando la consola
El proyecto está terminandose de adaptar a django para que cumpla con los Requisitos

La logica del juego se puede probar ejecutando unicamente el archivo main.py

``` 
python main.py
```

# Requisitos 


Los requisitos mínimos a cumplir son:
● Permitir Jugar a 2 Players y validar el orden.
● Validar la entrada e impedir movimientos no válidos.
● Visualizar el estado del tablero y comprobar si se ha producido un ganador.
● Usar git para subir el código a un repositorio público (github o bitbucket)
Requisitos valorables
● Implementar el juego usando un API REST y usar curl/wget como cliente. 
● Llevar un control de partidas jugadas, incluida la puntuación.
● Realización de Test Unitarios.
● Establecer una persistencia para no perder el estado en caso de reinicio de 
servidor/aplicación.
● Establecer control de sesiones con autenticación para permitir múltiples 
partidas/jugadores.
● Registrar un log de partidas y dar la capacidad de ser consultado.

## Backend Requirements

* [Python](https://www.python.org/downloads/).
* [Django](https://www.djangoproject.com/download/).

# Instalacion 

1. Clona el repositorio a local:
```
git clone https://github.com/jhoninsuasti3/challenge-phicustech.git
```
2. Ve al directorio del proyecto
```
cd tu-proyecto
```
3. Instala las dependencias utilizando pip:
```
pip install -r requirements.txt
```
4. Realiza las migraciones para crear las tablas en la base de datos:
```
python manage.py makemigrations
python manage.py migrate
```
# Uso 
```
python manage.py runserver
```
1. Crea usuarios, jugadores y realiza otras configuraciones necesarias a través del panel de:

## APIs
* Registro de Usuario: `POST /register/`
* Inicio de Sesión: `POST /login/`
* Cierre de Sesión: `POST /logout/`
* Lista de Usuarios: `GET /users/`
* Iniciar Partida: `POST /api/iniciar_partida/`
* Realizar Movimiento: `POST /realizar_movimiento/<int:partida_id>/`


## Pruebas 

1. Utiliza herramientas como Postman o curl para probar las APIs.

#Register

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "email": "test@example.com"}' http://localhost:8000/tictactoe_game/register/

{"username": "bandido", "password": "Admin12345", "email": "bandido@dominio.com", "simbolo": "X"}

#Login

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:8000/tictactoe_game/login/


#Logout

curl -X POST -H "Authorization: Token c4594acff2e5f9348ee809169a87c545d8df1842" http://localhost:8000/tictactoe_game/logout/


curl -X POST -H "Content-Type: application/json" -d '{"username": "PACO", "password": "1234"}'  http://localhost:8000/tictactoe_game/logout/

{"username": "religion", "password": "Admin123456", "email": "religion@hotmail.com", "simbolo": "X"}



## Licencia


Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.



# Adicionales test
python manage.py test tictactoe_game.tests.HomePageViewTestCase.test_home_page_view_authenticated
