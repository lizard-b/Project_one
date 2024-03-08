from random import randint

BOARD_SIZE = 6
SHIPS_TYPES = [3, 2, 2, 1, 1, 1, 1]
purple = '\033[1;35m'
reset = '\033[0m'
blue = '\033[0;34m'
yellow = '\033[1;93m'
red = '\033[0;31m'
miss = '\033[0;37m'


class Color:
    def __init__(self, text, color):
        self.color = color
        self.text = text

    def set_color(self):
        return self.color + self.text + reset


class Sigh(object):

    empty_cell = Color('○', purple).set_color()
    ship_cell = Color('■', blue).set_color()
    destroyed_ship = Color('×', red).set_color()
    miss_cell = Color('•', miss).set_color()


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

    def is_strike(self, shot_dot):
        return shot_dot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [[Sigh.empty_cell] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", Sigh.empty_cell)
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, status=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if status:
                        self.field[cur.x][cur.y] = Sigh.miss_cell
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = Sigh.ship_cell
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = Sigh.destroyed_ship
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, status=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Попадание!")
                    return True

        self.field[d.x][d.y] = Sigh.miss_cell
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        human = self.random_board()
        pc = self.random_board()
        pc.hid = True

        self.ai = AI(pc, human)
        self.us = User(human, pc)

    @staticmethod
    def greet():
        welcome = """                                           
         __      __    ____   _____    ____   _   __   ____   _ ^ _     _____     ____   _ ^ _
        |  \    /  |  / _  \ | |_\ \  / /\_\ | | / /  / _  \ | | / |   |  ___|   / _  \ | | / |
        |   \  /   | | | | | | ____/ | |     | |/ /  | | | | | |/  |   | |____  | | | | | |/  |
        | |\ \/ /| | | |_| | | |     |  \/ / | |\ \  | |_| | |   / |   |  ___ | | |_| | |   / |
        |_| \__/ |_|  \____/ |_|      \___/  |_| \_\  \____/ |__/|_|   |_____/   \____/ |__/|_|
                                              
        """
        text = """
        Вас приветствует игра «Морской бой». Битва продолжается до 
        тех пор, пока не будет уничтожены все корабли одной из сторон.

        Координаты выстрела вводятся цифрами через пробел:
        \t координата по горизонтали (X), пробел, координата по вертикали (Y)
        """
        marks = """
        Обозначения:
            ■ - палуба
            • - промах / обводка корабля
            ○ - вода
            × - попадание
        """
        print(Color(welcome, red).set_color())
        print(text)
        print(marks)
        input('\n\tНажмите -= Enter =- для старта')

    def try_board(self):
        ship_lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for lens in ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lens, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Все корабли противника уничтожены! Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Все ваши корабли потоплены! Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()
