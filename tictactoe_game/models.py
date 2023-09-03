import random

class TicTacToe:
    def __init__(self):
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.jugadores = []
        self.jugador_actual = None

    def imprimir_tablero(self):
        print("  0   1   2")
        for i, fila in enumerate(self.tablero):
            print(i, end=' ')
            for j, casilla in enumerate(fila):
                print(f"| {casilla} ", end='')
                if j < 2:
                    print("|", end='')  # Agregar línea vertical entre las casillas
            print("|\n  -----------")

    def comprobar_ganador(self, jugador):
        for fila in self.tablero:
            if all(casilla == jugador for casilla in fila):
                return True
        for columna in range(3):
            if all(self.tablero[fila][columna] == jugador for fila in range(3)):
                return True
        if all(self.tablero[i][i] == jugador for i in range(3)) or all(self.tablero[i][2 - i] == jugador for i in range(3)):
            return True
        return False

    def iniciar_juego(self):
        for i in range(2):
            nombre_jugador = input(f"Nombre del Jugador {i + 1}: ")
            self.jugadores.append((nombre_jugador, 'X' if i == 0 else 'O'))

        random.shuffle(self.jugadores)
        self.jugador_actual = self.jugadores[0]

        print(f"¡Bienvenido al juego Tic-Tac-Toe, {self.jugadores[0][0]} y {self.jugadores[1][0]}!")

    def jugar(self):
        for _ in range(9):
            self.imprimir_tablero()
            jugador_actual_nombre, jugador_actual_ficha = self.jugador_actual

            while True:
                try:
                    fila, columna = map(int, input(f"Turno de {jugador_actual_nombre} ({jugador_actual_ficha}): Ingrese fila y columna (0-2) separadas por espacio: ").split())
                    if 0 <= fila <= 2 and 0 <= columna <= 2 and self.tablero[fila][columna] == ' ':
                        self.tablero[fila][columna] = jugador_actual_ficha
                        break
                    else:
                        print("Movimiento no válido. Intente de nuevo.")
                except ValueError:
                    print("Entrada no válida. Ingrese dos números separados por espacio.")

            if self.comprobar_ganador(jugador_actual_ficha):
                self.imprimir_tablero()
                print(f"¡El jugador {jugador_actual_nombre} ({jugador_actual_ficha}) ha ganado!")
                return

            self.jugador_actual = self.jugadores[1] if self.jugador_actual == self.jugadores[0] else self.jugadores[0]

        self.imprimir_tablero()
        print("¡Empate!")

if __name__ == "__main__":
    juego = TicTacToe()
    juego.iniciar_juego()
    juego.jugar()
