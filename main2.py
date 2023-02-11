# Игра Морской Бой
from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "    1   2   3   4   5   6  "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    return True, ship.lives
                else:
                    return True, ship.lives
        self.field[d.x][d.y] = "."
        return False, None

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
                repeat, lives = self.enemy.shot(target)
                return repeat, target, lives
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        return d

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat, lives = self.enemy.shot(target)
                return repeat, target, lives
            except BoardException as e:
                pass


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
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        otstup = " " * 21
        print(otstup + "-------------------")
        print(otstup + "  Приветсвуем вас  ")
        print(otstup + "      в игре       ")
        print(otstup + "    морской бой    ")
        print(otstup + "-------------------")
        print(otstup + " формат ввода: x y ")
        print(otstup + " x - номер строки  ")
        print(otstup + " y - номер столбца ")
        print("\n Всего на доске: Трехтрубника 1, Двухтрубника 2, Однотрубника 4")

    def vivod_igr_pole(self):
        res = ""
        res += "    1   2   3   4   5   6" + " " * 15 + "1   2   3   4   5   6"
        for i in range(self.size):
            res_ai = " | ".join(self.ai.board.field[i]) + " |"
            if self.ai.board.hid:
                res_ai = res_ai.replace("■", "O")
            res_us = " | ".join(self.us.board.field[i]) + " |"
            res += f"\n{i + 1} | " + res_ai + " " * 9 + f"{i + 1} | " + res_us
        print("-" * 63)
        print("    Доска компьютера:" + " " * 19 + "Доска пользователя:")
        print(res)

    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                self.vivod_igr_pole()
                print("-" * 20)
                print("Ходит пользователь!")
                repeat, target, lives = self.us.move()
                if not repeat: print("Мимо!")
                if repeat: print("Корабль уничтожен!") if lives == 0 else print("Корабль ранен!")
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat, target, lives = self.ai.move()
                print(f"Ход компьютера: {target.x + 1} {target.y + 1}")
                if not repeat: print("Мимо!")
                if repeat: print("Корабль уничтожен!") if lives == 0 else print("Корабль ранен!")
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                self.vivod_igr_pole()
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                self.vivod_igr_pole()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()