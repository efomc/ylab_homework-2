from tkinter import *
from tkinter import messagebox
from random import choice
from collections import OrderedDict

game_window = Tk()  # окно игры
game_field = []  # поле с клетками
# текстовое поле с игровыми сообщениями
game_message_label = Label(game_window, font=("Arial Bold", 15))
game_status_dict = {
    "stop_game": False,  # маркер продолжения игры
    "last_computer_move": [],  # контейнер прошлого хода компьютера
}

# словарь знаков игроков и сообщений о победе/проигрыше
PLAYERS_SIGN_DICT = OrderedDict(
    {
        "human": {"char": "X", "loose_text": "Ты проиграл, человек"},
        "computer": {"char": "O", "loose_text": "Ты выиграл, человек"},
    }
)

CHECK_GRID = {
    "diagonal1": ((-1, -1), (1, 1)),
    "diagonal2": ((-1, 1), (1, -1)),
    "vertical": ((-1, 0), (1, 0)),
    "horizontal": ((0, -1), (0, 1)),
}


# проверяем доступные для хода ячейки
def check_free_cells():
    free_cells = []  # список с координатами пустых ячеек
    for line_number, line in enumerate(game_field):
        for column_number, cell in enumerate(line):
            # если ячейка пустая, добавляем ее координаты к списку
            if cell["text"] == "":
                free_cells.append((line_number, column_number))
    return free_cells


def check_human_move(line, column):
    if game_field[line][column]["text"]:  # проверка на свободную ячейку
        game_message_label["text"] = "Эта ячейка занята, человек, выбери другую."
    else:
        return line, column


def computer_move(char: str) -> tuple:
    free_cells = check_free_cells()
    line, column = None, None  # переменные координат хода
    while not line and not column:
        if len(free_cells) > 1:  # если есть куда ходить
            cell = choice(free_cells)  # случайный выбор варианта хода
            free_cells.remove(cell)  # удаление выбранного хода
            line, column = cell  # присвоение координатам выбранных значений
            if check_move_result((line, column), char):  # проверка на проигрыш
                line, column = None, None  # если ход ведет к проигрышу - новый цикл
        else:
            line, column = free_cells[0]  # если ход остался единственный - выбираем его
            break
    return line, column


def check_move_result(move_coordinates, char):
    for (
        row,
        directions,
    ) in CHECK_GRID.items():  # для всех направлений от выбранной ячейки
        loose_line = [move_coordinates]
        for direction in directions:
            check_possibility = True  # переключатель продолжения проверки
            check_coordinates = (
                move_coordinates  # возврат проверяемой ячейки к выбранной
            )
            while check_possibility:
                # получение координат проверяемой ячейки прибавлением поправок к ее координатам
                check_line, check_column = tuple(
                    item + correction
                    for item, correction in zip(check_coordinates, direction)
                )
                if 0 <= check_line <= 9 and 0 <= check_column <= 9:
                    if game_field[check_line][check_column]["text"] == char:
                        # если координаты в пределах решетки и проверяемый символ совпадает...
                        # прибавляем координаты к проигрышной линии
                        loose_line.append((check_line, check_column))
                        # и смещаем проверяемые координаты
                        check_coordinates = check_line, check_column
                        # если последовательность одинаковых символов достигает 5,
                        # то возвращаем результат хода - проигрыш
                        if len(loose_line) >= 5:
                            return loose_line
                    else:
                        check_possibility = False
                else:
                    check_possibility = False


def get_play_window():
    game_window.title("Крестики-нолики наоборот")  # заголовок для игрового окна
    start_message = "Твой ход первый, человек!"
    game_message_label["text"] = start_message  # приветственное сообщение
    # размещение поля с игровыми сообщениями в игровом окне
    game_message_label.grid(row=0, column=0, columnspan=10)
    # создание и размещение в игровом окне кнопки начала новой игры
    new_game_button = Button(
        game_window, text="Играть снова", command=lambda: new_game()
    )
    new_game_button.grid(row=10 + 1, column=0, columnspan=10, sticky="nsew")
    # заполнение игрового поля кнопками-ячейками
    for line in range(10):
        game_field.append([])
        for column in range(10):
            button = Button(
                game_window,
                text="",
                width=3,
                height=1,
                font=("Verdana", 20, "bold"),
                background="lavender",
                command=lambda row=line, col=column: click(row, col),
            )
            button.grid(row=line + 1, column=column, sticky="nsew")
            game_field[line].append(button)


def play_window():
    get_play_window()  # создание и запуск игрового окна
    game_window.mainloop()  # бесконечный цикл игрового окна


def new_game():
    game_message_label["text"] = "Ну попробуй еще раз!"  # сообщение начала новой игры
    for line in game_field:  # очистка игрового поля
        for cell in line:
            cell["text"] = ""
            cell["background"] = "lavender"
    game_status_dict["stop_game"] = False  # перезапуск маркера остановки игры...
    # ...и перезапуск метки последнего хода компьютера
    game_status_dict["last_computer_move"] = []


def click(line, column):
    # если игра не остановлена...
    if not game_status_dict["stop_game"]:
        if check_human_move(line, column):  # ...и человек выбрал пустое поле
            for player in PLAYERS_SIGN_DICT:  # сначала ходит человек, потом компьютер
                # назначение игрового значка для игрока
                char = PLAYERS_SIGN_DICT[player]["char"]
                if player == "computer":
                    line, column = computer_move(char)  # ход компьютера
                    # метка нового хода компьютера
                    game_field[line][column]["background"] = "grey"
                    # если был прошлый ход компьютера
                    if len(game_status_dict["last_computer_move"]):
                        last_line, last_column = game_status_dict["last_computer_move"]
                        # очистка цвета поля старого хода
                        game_field[last_line][last_column]["background"] = "lavender"
                    # обновление метки старого хода компьютера
                    game_status_dict["last_computer_move"] = [line, column]
                    # обновление игрового сообщения
                    game_message_label["text"] = "Делай свой ход, человек!"
                # отметка результата хода на доске
                game_field[line][column]["text"] = char
                # проверка линии в 5 знаков
                loose_line = check_move_result((line, column), char)
                # если набралось 5 знаков в ряд, вывести сообщение о победителе
                if loose_line:
                    game_message_label["text"] = PLAYERS_SIGN_DICT[player]["loose_text"]
                    # пометить проигрышную линию розовым
                    for (line, column) in loose_line:  
                        game_field[line][column]["background"] = "pink"
                    # маркер остановки игры на "стоп"
                    game_status_dict["stop_game"] = True
                    break
                # если для хода ячеек не осталось - ничья
                elif not len(check_free_cells()) and not game_status_dict["stop_game"]:
                    game_message_label["text"] = "Ничья"
                    game_status_dict["stop_game"] = True
                    break
    else:
        # если игра закончена - ход больше сделать нельзя и диалоговое окно об этом
        messagebox.showinfo("Усе!", 'Хочешь проиграть - жми "Играть снова!"')


def main():
    play_window()  # запуск игрового окна


if __name__ == "__main__":
    main()
