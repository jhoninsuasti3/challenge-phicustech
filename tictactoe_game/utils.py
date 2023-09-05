class TicTacToeGame:
    def __init__(self, jugador_1_nombre, jugador_2_nombre):
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.jugadores = [jugador_1_nombre, jugador_2_nombre]
        self.turno = 0
        self.movimientos_realizados = set()

    # Método para realizar un movimiento
    def realizar_movimiento_web(self, fila, columna, jugador):
        if (fila, columna) in self.movimientos_realizados or fila < 0 or fila > 2 or columna < 0 or columna > 2:
            return False  # Movimiento inválido
        if self.jugadores[self.turno % 2] != jugador:
            return False  # El jugador no tiene el turno
        if self.tablero[fila][columna] != " ":
            return False  # Casilla ocupada

        # Coloca la ficha del jugador en el tablero
        self.tablero[fila][columna] = "X" if self.turno % 2 == 0 else "O"
        self.movimientos_realizados.add((fila, columna))
        self.turno += 1  # Cambia el turno al siguiente jugador
        return True

    # Método para verificar si hay un ganador
    def verificar_ganador(self):
        # Verificar filas
        for fila in self.tablero:
            if all(cell == "X" for cell in fila):
                return self.jugadores[0]
            elif all(cell == "O" for cell in fila):
                return self.jugadores[1]

        # Verificar columnas
        for col in range(3):
            if all(self.tablero[row][col] == "X" for row in range(3)):
                return self.jugadores[0]
            elif all(self.tablero[row][col] == "O" for row in range(3)):
                return self.jugadores[1]

        # Verificar diagonales
        if all(self.tablero[i][i] == "X" for i in range(3)) or all(self.tablero[i][2 - i] == "X" for i in range(3)):
            return self.jugadores[0]
        if all(self.tablero[i][i] == "O" for i in range(3)) or all(self.tablero[i][2 - i] == "O" for i in range(3)):
            return self.jugadores[1]

        return None

    # Método para verificar si el juego ha terminado en empate
    def juego_terminado(self):
        return len(self.movimientos_realizados) == 9

    # Método para serializar el estado del juego
    def serializar_estado(self):
        estado = {
            'tablero': self.tablero,
            'turno': self.jugadores[self.turno % 2],
            'jugador_1': self.jugadores[0],
            'jugador_2': self.jugadores[1],
            'ganador': self.verificar_ganador(),
            'juego_terminado': self.juego_terminado(),
        }
        return estado
