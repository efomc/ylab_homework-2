from random import choice

PLAYERS_SIGN_DICT = {
    False: "O",
    True: "X",
}

CHECK_GRID = {
    "diagonal1": ((-1, -1), (1, 1)),
    "diagonal2": ((-1, 1), (1, -1)),
    "vertical": ((-1, 0), (1, 0)),
    "horizontal": ((0, -1), (0, 1)),
}


def generate_play_deck() -> list:
    return [
        ["_" for _ in range(10)] for _ in range(10)
    ]  # решетка 10*10 заполненная пустыми "_"


# печатаем игровое поле с разметкой осей Y и X от 1 до 10
def print_play_deck(play_deck: list):
    print("Y")
    for index, line in enumerate(play_deck):
        if index:
            print(10 - index, " | " + "  ".join(line) + " |")
        else:
            print(10 - index, "| " + "  ".join(line) + " |")
    print(
        "     "
        + "  ".join((str(column_number) for column_number in range(1, 11)))
        + " X"
    )


# проверяем доступные для хода ячейки
def check_free_cells(play_deck):
    free_cells = []  # список с координатами пустых ячеек
    for line_number, line in enumerate(play_deck):
        for column_number, cell in enumerate(line):
            # если ячейка пустая, добавляем ее координаты к списку
            if cell == "_":
                free_cells.append((line_number, column_number))
    return free_cells


# ход любого игрока
def move(play_deck: list, player: bool, char: str) -> tuple:
    free_cells = check_free_cells(play_deck)  # проверяем доступные для хода ячейки
    if len(free_cells):
        if player:
            # ход игрока и проверка его хода
            play_deck, result = human_move(play_deck, char)
            if result:
                result = "Компьютер выиграл!"
        else:
            # ход компьютера и проверка его хода
            play_deck, result = computer_move(play_deck, free_cells, char)
            if result:
                result = "Человек выиграл!"
    else:
        result = "Ничья!"  # если ходить больше некуда - ничья
    return play_deck, result


def get_human_move(play_deck: list) -> tuple:
    move_request = "Куда ходим? Введите координаты хода - Х и Y: "
    line, column = None, None  # переменные координат хода
    while not line and not column:
        try:
            # получение от пользователя целочисленных значений
            column, line = (int(item) - 1 for item in input(move_request).split())
        except (IndexError, ValueError):
            print("Надо вводить числа!")
        else:
            line = 9 - line  # превращение оси Y в индекс линии в массиве игровой доски
            if (
                0 <= line <= 9 and 0 <= column <= 9
            ):  # проверка на размер введенных чисел
                if play_deck[line][column] in (
                    "X",
                    "O",
                ):  # проверка на свободную ячейку
                    print("Эта ячейка занята, выберете другую.")
                else:
                    return line, column
            else:
                print("Координаты должны быть от 1 до 10!")
        line, column = (
            None,
            None,
        )  # если значения игрока не были приняты - возврат на новый цикл


def human_move(play_deck: list, char: str) -> tuple:
    move_line, move_column = get_human_move(
        play_deck
    )  # получаем от игрока координаты хода
    print(f"Человек сделал ход на {move_column + 1, 10 - move_line}")
    play_deck[move_line][move_column] = char  # отметка хода на доске
    result = check_move_result(
        play_deck, (move_line, move_column), char
    )  # проверка на проигрыш
    return play_deck, result


def computer_move(play_deck: list, free_cells: list, char: str) -> tuple:
    line, column = None, None  # переменные координат хода
    while not line and not column:
        if len(free_cells) > 1:  # если есть куда ходить
            cell = choice(free_cells)  # случайный выбор хода
            free_cells.remove(cell)  # удаление выбранного хода
            line, column = cell  # присвоение координатам выбранных значений
            if check_move_result(
                play_deck, (line, column), char
            ):  # проверка на проигрыш
                line, column = None, None  # если ход ведет к проигрышу - новый цикл
        else:
            line, column = free_cells[0]  # если ход остался единственный - выбираем его
            break
    print(f"Компьютер сделал ход на {column + 1, 10 - line}")
    result = check_move_result(
        play_deck, (line, column), char
    )  # проверка результата хода
    play_deck[line][column] = char  # отметка хода на доске
    return play_deck, result


def check_move_result(play_deck, move_coordinates, char):
    for (
        row,
        directions,
    ) in CHECK_GRID.items():  # для всех направлений от выбранной ячейки
        row_count = 0  # счетчик последовательных символов в линии
        for direction in directions:
            check_possibility = True  # переключатель продолжения проверки
            check_coordinates = (
                move_coordinates  # возврат проверяемой ячейки к выбранной
            )
            while check_possibility:
                # получение координат проверяемой ячейки прибавлением  поправок к ее координатам
                check_line, check_column = tuple(
                    item + correction
                    for item, correction in zip(check_coordinates, direction)
                )
                if 0 <= check_line <= 9 and 0 <= check_column <= 9:
                    if play_deck[check_line][check_column] == char:
                        # если координаты в пределах решетки и проверяемый символ совпадает...
                        row_count += 1  # счетчик увеличиваем на 1...
                        # и смещаем проверяемые координаты
                        check_coordinates = check_line, check_column
                        # если последовательность одинаковых символов достигает 4,
                        # (а вместе с проверяемой ячейкой - 5),
                        # то возвращаем результат хода - проигрыш
                        if row_count == 4:
                            return "loose"
                    else:
                        check_possibility = False
                else:
                    check_possibility = False


def game_round():
    play_deck = generate_play_deck()  # создаем игровое поле
    print_play_deck(play_deck)  # печатаем игровое поле
    stop_game = False  # маркер продолжения игры
    player = True  # выбор игрока
    while not stop_game:  # пока игра не остановлена...
        char = PLAYERS_SIGN_DICT.get(player)  # забираем значок игрока
        play_deck, move_result = move(play_deck, player, char)  # делаем ход игрока
        print_play_deck(play_deck)  # выводим доску с новым ходом
        # если есть результат (проигрыш) останавливаем игру, печатаем результат
        if move_result:
            print(move_result)
            stop_game = True
        player = not player  # если игра не остановлена - смена игрока и новый цикл


def main():
    game_round()


if __name__ == "__main__":
    main()
