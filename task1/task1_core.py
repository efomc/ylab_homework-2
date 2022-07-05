from re import findall
from itertools import permutations


# запрос у пользователя и обработка списка координат
def get_coordinates_simple():
    # запрос у пользователя списка координат в виде простой строки
    raw_data_coordinates = input(
        "введите координаты стартовой точки и всего маршрута: "
    ).split("[ ,()]")
    # перевод строки от пользователя в итератор по списку из целых чисел
    int_raw_coordinates = iter([int(item) for item in raw_data_coordinates])
    # объединение элементов списка (координат) попарно
    return [(item, next(int_raw_coordinates)) for item in int_raw_coordinates]


# запрос у пользователя и обработка списка координат
def get_coordinates():
    # запрос у пользователя списка координат, поиск в строке и возврат всех пар чисел
    raw_data_coordinates = findall(
        r"(\d+\D+\d+)",
        input(
            "Введите координаты стартовой точки "
            "и остальных точек маршрута объединенные попарно скобками: "
        ),
    )
    # распознавание чисел в каждой паре, возврат списка из кортежей с парами координат
    return [
        tuple(int(coordinate) for coordinate in findall(r"\d+", item))
        for item in raw_data_coordinates
    ]


# вычисление и возврат расстояния между точками
def calc_distance(point1: tuple, point2: tuple) -> float:
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5


# вычисление длины маршрута
def calc_route_lenth(route_list: list):
    max_index = len(route_list)  # количество точек маршрута
    return sum(
        [
            calc_distance(point, route_list[index + 1])
            for index, point in enumerate(route_list)
            if index + 1 < max_index
        ]
    )


# построение вариантов маршрута
def get_route_variants(points_list: list) -> list:
    start_point = points_list[0]  # начальная и конечная точки
    route_points_list = points_list[1:]  # все точки, кроме начальной
    route_variants = permutations(
        route_points_list, len(route_points_list)
    )  # построение вариантов комбинаций точек
    # возврат списка итоговых вариантов маршрута начинающихся и заканчивающихся стартовой точкой
    return [[start_point] + list(variant) + [start_point] for variant in route_variants]


# выбор наикратчайшего пути
def get_shortest_route(route_variants: list) -> list:
    min_lenth = calc_route_lenth(route_variants[0])  # стартовое значение для длины пути
    min_route = route_variants[0]  # стартовый путь
    # перебираем все варианты пока не найдем самый короткий
    for route in route_variants:
        route_lenth = calc_route_lenth(route)
        if route_lenth < min_lenth:
            min_lenth = route_lenth
            min_route = route
    return min_route  # возвращаем маршрут с минимальной длиной


def get_rote_description(route: list):
    route_description = f"{route[0]}"  # начало описания - первая точка
    max_index = len(route)  # количество точек маршрута
    route_lenth = 0
    for index, point in enumerate(route):
        if index + 1 < max_index:
            # увеличение длины маршрута на расстояние до следующей точки, если она есть
            route_lenth += calc_distance(point, route[index + 1])
            # добавление описания следующей точки и суммарного расстояния
            route_description += f" -> {route[index + 1]}[{route_lenth}]"
    return (
        route_description + f" = {route_lenth}"
    )  # возврат строки с итоговым расстоянием


def main():
    points_list = get_coordinates()  # получаем набор точек в виде списка пар координат
    route_variants = get_route_variants(points_list)  # строим набор вариантов маршрутов
    shortest_route = get_shortest_route(
        route_variants
    )  # получаем самый короткий маршрут
    print(get_rote_description(shortest_route))  # вывод описания выбранного маршрута


if __name__ == "__main__":
    main()
