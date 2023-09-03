
class TicTacToeGame:
    def __init__(self):
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.jugadores = []
        self.turno = 0
        self.movimientos_realizados = set()

    def imprimir_tablero(self):
        print("  0   1   2")
        for i, fila in enumerate(self.tablero):
            print(f"{i} {' | '.join(fila)}")
            if i < 2:
                print("  " + "-" * 9)

    def verificar_ganador(self, jugador):
        # Verificar filas
        for fila in self.tablero:
            if all(cell == jugador for cell in fila):
                return True
        # Verificar columnas
        for col in range(3):
            if all(self.tablero[row][col] == jugador for row in range(3)):
                return True
        # Verificar diagonales
        if all(self.tablero[i][i] == jugador for i in range(3)) or all(self.tablero[i][2 - i] == jugador for i in range(3)):
            return True
        return False

    def realizar_movimiento(self, fila, columna, ficha):
        if self.tablero[fila][columna] != " ":
            return False  # Casilla ocupada
        self.tablero[fila][columna] = ficha
        self.movimientos_realizados.add((fila, columna))
        return True

    def juego_terminado(self):
        return len(self.movimientos_realizados) == 9

    def jugar(self):
        self.jugadores.append(input("Ingresa el nombre del Jugador 1 (X): "))
        self.jugadores.append(input("Ingresa el nombre del Jugador 2 (O): "))

        while True:
            jugador_actual = self.jugadores[self.turno % 2]
            ficha = "X" if self.turno % 2 == 0 else "O"

            self.imprimir_tablero()
            print(f"Turno de {jugador_actual} ({ficha})")
            print("Ingresa tu movimiento en el formato 'fila,columna'.")

            movimiento = input()
            try:
                fila, columna = map(int, movimiento.split(","))
            except ValueError:
                print("Entrada no válida. Utiliza el formato 'fila,columna'.")
                continue

            if (fila, columna) in self.movimientos_realizados or fila < 0 or fila > 2 or columna < 0 or columna > 2:
                print("Movimiento inválido. Inténtalo de nuevo.")
            else:
                if self.realizar_movimiento(fila, columna, ficha):
                    if self.verificar_ganador(ficha):
                        self.imprimir_tablero()
                        print(f"{jugador_actual} ({ficha}) gana. ¡Felicidades!")
                        return
                    if self.juego_terminado():
                        self.imprimir_tablero()
                        print("El juego terminó en empate.")
                        return
                    self.turno += 1
