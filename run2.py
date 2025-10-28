import sys
from collections import deque
from typing import List, Dict, Tuple, Optional


def bfs(edges: Dict[str, list], start: str) -> Optional[Tuple[str, str]]:
    """
        Idea:
            Пробегаемся бфсом в поиске шлюза.
            Если нашли шлюз, не возвращаем, а складываем в массив ответов.
            Затем среди них выберем лексикографически меньший. Его и вернем.
    :param edges: Словарь смежности ребер
    :param start: стартовая точка
    :return: кортеж из 3х элементов:
     (Шлюз, Откуда в этот шлюз попали)
    """
    q = deque([(start, node, 1) for node in sorted(edges[start])])
    visited = {start}
    founded = []
    min_depth = None

    while q:
        from_node, current_node, depth = q.popleft()
        if current_node.isupper():
            # Проверки нового шлюза на закрытие
            if min_depth is None:
                min_depth = depth
            if depth == min_depth:
                founded.append((current_node, from_node))
            continue

        if current_node not in visited:
            visited.add(current_node)
            for neighbour in sorted(edges[current_node]):
                q.append((current_node, neighbour, depth + 1))

    if not founded:
        return None

    founded.sort(key=lambda x: (x[0], x[1]))
    return founded[0]


def bfs_next_step(edges: Dict[str, List[str]], start: str) -> Optional[str]:
    """
        Idea:
            Ищем следующий ход нашего вируса,
            в зависимости от изменений в лабиринте, и нового расположения шлюзов
            Запоминаем первый ход, чтобы вернуть его в конце, после того,
            как нашли шлюз.
    :param edges: Словарь смежности ребер
    :param start: стартовая точка
    :return: строка - нода следующего хода вируса
    """
    q = deque([(node, node) for node in sorted(edges[start])])
    visited = {start}
    while q:
        first_step_node, current_node = q.popleft()
        if current_node.isupper():
            return first_step_node
        if current_node not in visited:
            visited.add(current_node)
            for neighbour in sorted(edges[current_node]):
                q.append((first_step_node, neighbour))
    return None


def solve(edges: Dict[str, List[str]]) -> List[str]:
    """
        Idea:
            Симуляция движения вируса и удаления шлюзов.
            Как только убрали все опасные шлюзы - return
    :param edges: Словарь смежности ребер
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    result = []
    current_pos = 'a'
    while True:
        founded = bfs(edges, current_pos)  # Нашли удаленный шлюз
        if not founded:
            return result
        gateway, from_node = founded
        result.append(f'{gateway}-{from_node}')  # Добавили удаленный шлюз

        # Почистили лабиринт
        edges[gateway].remove(from_node)
        edges[from_node].remove(gateway)

        # Поменяли позицию вируса
        current_pos = bfs_next_step(edges, current_pos)
        if not current_pos:
            return result


def main():
    edges = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.setdefault(node1, []).append(node2)
                edges.setdefault(node2, []).append(node1)
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
