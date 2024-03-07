from random import randint
from time import sleep

BOARD_SIZE = 6
SHIPS_TYPES = [3, 2, 2, 1, 1, 1, 1]


class BoardException(Exception):

    pass


class BoardOutException(BoardException):

    def __str__(self) -> str:

        return '\n\tЭта точка за пределами игровой доски!\n'


class BoardUsedException(BoardException):

    def __str__(self) -> str:

        return '\n\tВы уже стреляли в эту точку!\n'


class BoardWrongShipException(BoardException):

    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:

    def __init__(self, bow, length, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            exec_x, exec_y = self.bow.x, self.bow.y

            if self.direction == 0:
                exec_x += i
            elif self.direction == 1:
                exec_y += i

            ship_dots.append(Dot(exec_x, exec_y))
        return ship_dots

    def is_strike(self, dot):
        return dot in self.dots


class Board:
    _is_hidden: bool = False

    def __init__(self) -> None:
        self.table = [['○'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ships = list()
        self.locked_dots = list()
        self.live_ships = len(SHIPS_TYPES)

    @property
    def is_hidden(self) -> bool:
        """
        Геттер для параметра _is_hidden
        """

        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        Сеттер для параметра _is_hidden
        """

        if isinstance(value, bool):
            self._is_hidden = value
        else:
            raise ValueError('Параметр is_hidden должен быть True или False.')

    def add_ship(self, ship: Ship) -> None:
        """
        Ставит корабль на доску (если не получается, выбрасывает исключение).
        """

        # Проверяем возможность установки всех точек корабля
        for dot in ship.dots:
            if Board.out(dot) or dot in self.locked_dots:
                raise BoardWrongShipException()
        # Устанавливаем на доску корабль
        for dot in ship.dots:
            self.table[dot.x][dot.y] = '■'
            self.locked_dots.append(dot)
        # Добавляем корабль в список кораблей доски
        self.ships.append(ship)
        # Отмечаем ореол корабля
        self.mark_oreol(ship)

    def mark_oreol(self, ship: Ship, is_game: bool = False) -> None:
        # Смещения координат для нахождения всех соседей данной точки
        neighbours = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                      (1, 0), (-1, 1), (0, 1), (1, 1)]
        # Для каждой точки корабля и для всех её соседей
        for dot in ship.dots:
            for dx, dy in neighbours:
                x, y = dot.x + dx, dot.y + dy
                current_dot = Dot(x, y)
                # Если сосед в пределах доски и не был помечен ранее
                if (not Board.out(current_dot)) and \
                   (current_dot not in self.locked_dots):
                    # Помечаем соседа
                    self.locked_dots.append(current_dot)
                    # Если идёт игра, отмечаем ореол на доске
                    if is_game:
                        self.table[x][y] = '•'

    def show(self) -> None:
        print(' X| 1 2 3 4 5 6')
        print('Y◢ ____________')
        for row in range(BOARD_SIZE):
            print(row + 1, end=' | ')
            for col in range(BOARD_SIZE):
                cell = self.table[col][row]
                if self.is_hidden:
                    # Прячем ещё живые корабли соперника
                    print('○', end=' ') if cell == '■' else print(cell, end=' ')
                else:
                    print(cell, end=' ')
            print('')
        print('\n')

    @staticmethod
    def out(dot: Dot) -> bool:
        return not (0 <= dot.x < BOARD_SIZE and 0 <= dot.y < BOARD_SIZE)

    def shot(self, dot: Dot) -> bool:
        # Если выстрел за пределы доски
        if Board.out(dot):
            raise BoardOutException
        # Если выстрел в уже стрелянную точку
        if dot in self.locked_dots:
            raise BoardUsedException
        # Добавляем точку в список уже стрелянных
        self.locked_dots.append(dot)
        # Для каждого корабля на доске
        for ship in self.ships:
            # Если есть попадание
            if ship.is_strike(dot):
                # Отнимаем жизнь у корабля
                ship.lives -= 1
                # Помечаем точку на доске
                self.table[dot.x][dot.y] = '×'
                # Если это потопление
                if ship.lives == 0:
                    # Уменьшаем количество живых кораблей
                    self.live_ships -= 1
                    # Отмечаем ореол вокруг потопленного корабля
                    self.mark_oreol(ship, is_game=True)
                    # Сообщаем о потоплении
                    print('\n\tКорабль потоплен!')
                    sleep(1)
                    # У текущего игрока сохраняется право следующего хода
                    return True
                # Попал, но не потопил
                else:
                    # Сообщаем о попадании
                    print('\n\tПопадание!')
                    sleep(1)
                    # У текущего игрока сохраняется право следующего хода
                    return True
        # Нет попадания
        # Помечаем точку на доске
        self.table[dot.x][dot.y] = '•'
        # Сообщаем о промахе
        print('\n\tМимо.')
        sleep(1)
        # Право следующего хода переходит сопернику
        return False

    def get_ready(self) -> None:
        self.locked_dots = list()

    def is_loser(self) -> bool:
        return self.live_ships == 0


class Player():
    def __init__(self, own_board: Board, opponent_board: Board) -> None:
        self.own_board = own_board
        self.opponent_board = opponent_board

    def ask(self):
        raise NotImplementedError(f'Определите ask в {self.__class__.__name__}.')

    def move(self) -> bool:
        while True:
            try:
                return self.opponent_board.shot(self.ask())
            except ValueError:
                print('\n\tВнимательнее, вводите две цифры через пробел.\n')
                sleep(1)
            except BoardException as e:
                print(e)
                sleep(1)


class AI(Player):
    def ask(self) -> Dot:
        x, y = randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)
        print(f'x y = {x} {y}')
        sleep(1)
        return Dot(x - 1, y - 1)


class User(Player):
    def ask(self) -> Dot:
        x, y = input('x y = ').strip().split()
        if x and y:
            return Dot(int(x) - 1, int(y) - 1)
        else:
            raise ValueError


class Game():
    def __init__(self) -> None:
        self.user_board = self.make_board()
        self.ai_board = self.make_board()
        self.ai_board.is_hidden = True
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def make_board(self) -> Board:
         board = None
        while board is None:
            board = Game.random_board()
        board.get_ready()
        return board

    @staticmethod
    def random_board() -> Board:
        # Создаём пустую доску
        board = Board()
        # Устанавливаем счётчик попыток
        attempts = 0
        # Для каждого типа корабля, от самого большого к самому маленькому
        for length in SHIPS_TYPES:
            # Начинаем попытки поставить корабль
            while True:
                # Если число попыток превышено, то сдаёмся и начинаем заново
                if attempts > 2000:
                    return None
                # Пытаемся поставить нос корабля в случайную точку и
                # расположить его в случайном направлении
                try:
                    board.add_ship(Ship(length,
                                        Dot(randint(0, BOARD_SIZE-1),
                                            randint(0, BOARD_SIZE-1)
                                            ),
                                        randint(0, 1)
                                        )
                                   )
                    break
                except BoardWrongShipException:
                    pass
                # Увеличиваем счётчик попыток
                attempts += 1
        # Возвращаем доску с расставленными кораблями
        return board

    @staticmethod
    def greet() -> None:
        logo = """
         ____        _   _   _           _     _          _____
        |  _ \      | | | | | |         | |   (_)        / ____|
        | |_) | __ _| |_| |_| | ___  ___| |__  _ _ __   | |  __  __ _ _ __ ___   ___
        |  _ < / _` | __| __| |/ _ \/ __| '_ \| | '_ \  | | |_ |/ _` | '_ ` _ \ / _ \
        | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) | | |__| | (_| | | | | | |  __/
        |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/   \_____|\__,_|_| |_| |_|\___|
                                                | |
                                                |_|
        """
        text = """
        Привет! Это «Морской бой». Правила ты знаешь.
        Бой идёт до полного уничтожения одной из сторон.
        К счастью для тебя, компьютер пуляет просто наугад.

        Координаты выстрела вводятся цифрами через пробел:
        \t координата по горизонтали (X), пробел, координата по вертикали (Y)
        """
        marks = """
        Обозначения:
            ■ - палуба
            • - мимо / ореол корабля
            ○ - море
            × - попадание
        """
        print(logo)
        print(text)
        print(marks)
        input('\n\tНажмите -= Enter =- для старта')

    def show_boards(self) -> None:
        print('\n\n\n' + '-' * 50)
        print('Доска пользователя:\n')
        self.user.own_board.show()
        print('Доска компьютера:\n')
        self.ai.own_board.show()

    def loop(self) -> None:
        # Маркер текущего игрока
        player = 0
        # Игровой цикл
        while True:
            # Выводим на экран доски обоих игроков
            self.show_boards()
            # Делаем ход текущим игроком
            if player % 2 == 0:
                print('Ваш ход:')
                repeat = self.user.move()
            else:
                print('Ходит компьютер:')
                repeat = self.ai.move()
            # Переход / сохранение права следующего хода
            player += 0 if repeat else 1
            # Если игрок-компьютер проиграл
            if self.ai.own_board.is_loser():
                print('\n\n\n' + '-' * 50 + '\n\n\n')
                print('#' * 22 + '\n#    Вы выиграли!    #\n' + '#' * 22)
                self.show_boards()
                break
            # Если игрок-пользователь проиграл
            if self.user.own_board.is_loser():
                print('\n\n\n' + '-' * 50 + '\n\n\n')
                print('#' * 22 + '\n# Компьютер выиграл! #\n' + '#' * 22)
                self.show_boards()
                break

    def start(self) -> None:
        Game.greet()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()
