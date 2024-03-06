import random


class SeaBattleGame:
    def __init__(self):
        self.board_size = 6
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pc_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = {'Подлодка': 3, 'Истребитель': 2, 'Катер': 1}
        self.pc_ships = {'Подлодка': 3, 'Истребитель': 2, 'Катер': 1}

    def print_boards(self):
        print("   Player Board          Computer Board")
        print("   1 2 3 4 5 6            1 2 3 4 5 6")
        print("  -------------          -------------")
        for i in range(self.board_size):
            print(
                f"{chr(65 + i)}|{' '.join(self.player_board[i])} |        {chr(65 + i)}|{' '.join(self.pc_board[i])} |")

    def place_ships(self, board, ships):
        for ship, size in ships.items():
            print(f"Расставьте корабль '{ship}' ({size} клеток):")
            while True:
                try:
                    orientation = input("Выберите ориентацию (горизонтально/вертикально): ").lower()
                    if orientation not in ('горизонтально', 'вертикально'):
                        raise ValueError("Неверный ввод. Попробуйте снова.")
                    start_pos = input("Введите начальные координаты (например, A3): ").upper()
                    if len(start_pos) != 2 or not ('A' <= start_pos[0] <= chr(65 + self.board_size - 1)) or not (
                            '1' <= start_pos[1] <= str(self.board_size)):
                        raise ValueError("Неверный формат ввода. Попробуйте снова.")
                    start_row, start_col = ord(start_pos[0]) - 65, int(start_pos[1]) - 1

                    if orientation == 'горизонтально' and all(
                            board[start_row][start_col + i] == ' ' for i in range(size)):
                        for i in range(size):
                            board[start_row][start_col + i] = 'O'
                        break
                    elif orientation == 'вертикально' and all(
                            board[start_row + i][start_col] == ' ' for i in range(size)):
                        for i in range(size):
                            board[start_row + i][start_col] = 'O'
                        break
                    else:
                        raise ValueError("Корабль не может быть размещен здесь. Попробуйте снова.")
                except ValueError as e:
                    print(e)

    def play(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        self.place_ships(self.player_board, self.ships)
        self.place_ships(self.pc_board, self.pc_ships)

        while any('O' in row for row in self.player_board) and any('O' in row for row in self.pc_board):
            self.print_boards()
            self.player_turn()
            if any('O' in row for row in self.pc_board):
                self.pc_turn()

        self.print_boards()
        if not any('O' in row for row in self.pc_board):
            print("Вы победили! Все корабли компьютера уничтожены.")
        else:
            print("Вы проиграли! Ваши корабли потоплены.")

    def player_turn(self):
        print("\nВаш ход!")
        while True:
            try:
                guess = input("Введите координаты выстрела (например, A3): ").upper()
                if len(guess) != 2 or not ('A' <= guess[0] <= chr(65 + self.board_size - 1)) or not (
                        '1' <= guess[1] <= str(self.board_size)):
                    raise ValueError("Неверный формат ввода. Попробуйте снова.")
                row, col = ord(guess[0]) - 65, int(guess[1]) - 1
                if self.pc_board[row][col] != ' ':
                    raise ValueError("Вы уже стреляли в эту клетку. Попробуйте снова.")
                break
            except ValueError as e:
                print(e)

        if self.pc_board[row][col] == 'O':
            print("Попадание!")
            self.pc_board[row][col] = 'X'
        else:
            print("Мимо!")
            self.pc_board[row][col] = '-'

    def pc_turn(self):
        print("\nХод компьютера!")
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if self.player_board[row][col] == ' ':
                break

        if self.player_board[row][col] == 'O':
            print("Компьютер попал в ваш корабль!")
            self.player_board[row][col] = 'X'
        else:
            print("Компьютер промахнулся!")
            self.player_board[row][col] = '-'


game = SeaBattleGame()
game.play()
