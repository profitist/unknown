import heapq
import sys
from typing import Tuple, Generator, Self


class State:
    """
    Класс работы с состояниями лабиринта
    """
    ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}  # Энергия на шаг буквы
    # Пара: буква - комната
    ROOM_INDEX_BY_LETTER = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
    # Обратная пара: комната - буква
    LETTER_BY_ROOM_INDEX = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}

    # Разрешенные позиции в коридоре
    ALLOWED_HALL_POSITIONS = [0, 1, 3, 5, 7, 9, 10]

    def __init__(self, hall_and_rooms: str, depth: int) -> None:
        """
            Idea:
                Инициализация объекта состояния лабиринта
        :param hall_and_rooms: единая строка для кодирования состояния лабиринта
        :param depth: глубина комнат лабиринта
        __room_code_map - Удобная переменная для
        индекса в кодировке по индексу комнаты
        """
        self.code = hall_and_rooms  # Первые 11 индексов - холл, затем комнаты
        self.depth = depth
        self.__room_code_map = {
            2: 11,
            4: 11 + self.depth,
            6: 11 + self.depth * 2,
            8: 11 + self.depth * 3
        }

    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, other: object) -> bool:
        return self.code == other

    def find_neighbours(self) -> Generator[Tuple["State", int], None, None]:
        """Генерирует соседние состояния"""
        yield from self.find_paths_room_entry()
        yield from self.find_paths_room_exit()

    def find_paths_room_entry(self) -> \
            Generator[Tuple["State", int], None, None]:
        """
            Idea:
                Ищет все соседние состояния, где буква с
                коридора заходит в нужную комнату
        :return: Ленивый вывод соседей типа (зашел в комнату)
        """

        for hall_idx in range(11):
            element = self.code[hall_idx]
            if element == '.':
                continue
            target_idx = self.ROOM_INDEX_BY_LETTER[element]

            if not self.is_hall_empty(hall_idx, target_idx):
                continue
            if not self.is_room_correct(target_idx):
                continue

            # ищем место в комнате
            empty_room_place_idx = self.find_place_in_room(target_idx)
            new_state = self.move(hall_idx, empty_room_place_idx)

            # подсчет кол-ва шагов и стоимости
            steps = (abs(hall_idx - target_idx) +
                     (empty_room_place_idx - self.__room_code_map[
                         target_idx] + 1))
            cost = steps * self.ENERGY[element]

            yield new_state, cost

    def find_paths_room_exit(self) \
            -> Generator[Tuple["State", int], None, None]:
        """
            Idea:
                Ищет все соседние состояния, где буква с
                комнаты выходит в коридор
        :return: Ленивый вывод соседей типа (вышел в коридор)
        """
        # перебор всех комнат
        for room_abs_idx, room_code_idx in self.__room_code_map.items():
            for depth_in_room in range(self.depth):

                element = self.code[room_code_idx + depth_in_room]
                room_owner = self.LETTER_BY_ROOM_INDEX[room_abs_idx]

                # условие на то, что если элемент правильный по комнате, но
                # под ним есть другие некорректные элементы, то достаем его
                are_any_incorrect_under = any(
                    self.code[i + room_code_idx] != room_owner
                    for i in range(self.depth)
                )

                if (element != '.' and
                        (element != room_owner or are_any_incorrect_under)):
                    element_idx = room_code_idx + depth_in_room
                    break
            else:
                continue

            # куда достаем
            for hall_pos in self.ALLOWED_HALL_POSITIONS:
                if self.is_hall_empty(room_abs_idx, hall_pos):
                    # счет стоимости
                    steps = depth_in_room + 1 + abs(hall_pos - room_abs_idx)
                    new_state = self.move(element_idx, hall_pos)
                    cost = steps * self.ENERGY[element]

                    yield new_state, cost

    def is_hall_empty(self, start: int, finish: int) -> bool:
        """
            Idea:
                В коридоре в указанном диапазоне нет блокировок
                от других элементов
        :param start: откуда по коридору
        :param finish: куда по коридору
        :return: True или False
        """
        if start < finish:
            for i in range(start + 1, finish + 1):
                if self.code[i] != '.':
                    return False
        else:
            for i in range(finish, start):
                if self.code[i] != '.':
                    return False
        return True

    def is_room_correct(self, room_idx: int) -> bool:
        """
            Idea:
                Проверить что в комнате нет элементов, несоответствующих ей
                Делаем это перед вставкой элемента в комнату из коридора.
        :param room_idx:
        :return: True или False
        """
        room_code = self.__room_code_map[room_idx]
        for i in range(room_code, room_code + self.depth):
            c = self.code[i]
            if c != '.' and c != self.LETTER_BY_ROOM_INDEX[room_idx]:
                return False
        return True

    def move(self, first_pos: int, second_pos: int) -> Self:
        """
            Idea:
                Передвижение буквы в нужное место
        :param first_pos: откуда мы двигаем элемент
        :param second_pos: куда мы двигаем элемент
        Индексация по кодировке
        :return: new_state: новое состояние
        """
        ls = list(self.code)
        ls[first_pos], ls[second_pos] = ls[second_pos], ls[first_pos]
        return State(''.join(ls), self.depth)

    def find_place_in_room(self, room_idx: int) -> int:
        """
            Idea:
                Поиск места в комнате для вставки элемента из коридора
        :param room_idx: Индекс комнаты (В лабиринте, не в кодировке),
        куда хотим вставить элемент
        :return: Индекс в кодировке, куда будет произведена вставка элемента
        """
        room_code = self.__room_code_map[room_idx]
        for i in range(room_code, room_code + self.depth):
            if self.code[i] == '.':
                return i

    def __repr__(self) -> str:
        return self.code


def read_input() -> State:
    """
        Idea:
            Парсинг ввода.
    :return:
        State: начальное состояние в теле объекта State
    """
    lines = [line.rstrip('\n') for line in sys.stdin if line.strip()]
    hall = ''.join(lines[1][1:12])
    room_lines = [[line[i] for i in (3, 5, 7, 9)] for line in lines[2:-1]]
    depth = len(room_lines)
    rooms = ''.join(''.join(col) for col in zip(*room_lines))
    return State(hall + rooms, depth)


def solve(initial: State) -> int:
    """
        Решение задачи о сортировке в лабиринте

        Args:
            :param initial:
            Начальное состояние лабиринта
        Returns:
            минимальная энергия для достижения целевой конфигурации
        Idea:
            решение через алгоритм дейкстры для поиска минимального пути до
            корректного состояния лабиринта
    """
    depth = initial.depth
    goal_rooms = ''.join(c * depth for c in 'ABCD')
    goal_state = State('.' * 11 + goal_rooms, depth)
    state_id = 0
    heap = [(0, state_id, initial)]
    seen = {initial: 0}

    while heap:
        cost, _, state = heapq.heappop(heap)
        if state == goal_state:
            return cost
        for new_state, move_cost in state.find_neighbours():
            new_cost = cost + move_cost

            if new_state not in seen or new_cost < seen[new_state]:
                seen[new_state] = new_cost
                state_id += 1
                heapq.heappush(heap, (new_cost, state_id, new_state))
    return -1


def main() -> None:
    initial = read_input()
    answer = solve(initial)
    if answer == -1:
        print('Решение не найдено')
        return
    print(answer)


if __name__ == '__main__':
    main()
