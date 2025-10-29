import sys
from collections import deque
from typing import List, Dict, Set


def is_virus_closed(edges: Dict[str, set], start: str) -> bool:
    """
        Idea:
            Проверка на то, что вирус не может дойти до шлюза
    :param edges: Словарь смежности вершин
    :param start: Стартовая точка
    :return: bool да если не изолирован / нет иначе
    """
    q = deque([start])
    visited = {start}
    while q:
        node = q.popleft()
        if node.isupper():
            return False
        for neigh in edges[node]:
            if neigh not in visited:
                visited.add(neigh)
                q.append(neigh)
    return True


def can_isolate(edges: Dict[str, set], virus_pos: str, ans: List[str]) -> bool:
    """
        Idea:
            Проверка на то, что мы можем закрыть шлюз и затем найти
            решение для полученного графа
    :param edges:
    :param virus_pos:
    :param ans: Собираемый ответ на задачу
    :return: True если мы можем закрыть шлюз и затем найти решение
    для полученного графа
    """
    if is_virus_closed(edges, virus_pos):
        return True
    if virus_pos.isupper():
        return False
    gateways = sorted([node for node in edges if node.isupper()])
    for gateway in gateways:
        for neigh in sorted(edges[gateway]):
            break_halls(edges, gateway, neigh)
            next_pos = find_virus_next_step(edges, virus_pos)
            if not next_pos or can_isolate(edges, next_pos, ans):
                ans.append(f'{gateway}-{neigh}')
                rebuild_edges(edges, gateway, neigh)
                return True
            rebuild_edges(edges, gateway, neigh)
    return False


def find_virus_next_step(edges: Dict[str, Set[str]], start: str):
    """
        Idea:
            Поиск следующего хода вируса.
            бфс до ближайшего меньшего по лексике шлюза с наименьшим путем
    :param edges: Словарь смежности вершин
    :param start: Стартовая точка
    :return: result_first_step - Первый шаг бфс для найденного шлюза
    """
    q = deque([(node, node, 1) for node in edges[start]])
    visited = {start}
    min_depth = float('inf')
    founded_gate = ''
    result_first_step = ''
    while q:
        first_step, current_node, depth = q.popleft()

        if depth > min_depth:
            break

        if current_node.isupper():
            if depth < min_depth:
                min_depth = depth
                result_first_step = first_step
                founded_gate = current_node
            elif min_depth == depth:
                if current_node < founded_gate:
                    result_first_step = first_step
                elif current_node == founded_gate:
                    result_first_step = min(result_first_step, first_step)

        for neigh in sorted(edges[current_node]):
            if neigh not in visited:
                visited.add(neigh)
                q.append((first_step, neigh, depth + 1))
    return result_first_step


def solve(edges: Dict[str, Set[str]]) -> List[str]:
    """
        Idea:
            Рекурсивный спуск с перебором вариантов закрытия шлюзов
    :param edges: Словарь смежности вершин
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    result = []
    current_pos = 'a'
    can_isolate(edges, current_pos, result)
    return result[::-1]


def break_halls(edges: Dict[str, Set[str]], gateway: str, node: str) -> None:
    """
        Idea:
            Очистка коридоров после закрытия шлюза
    :param edges: Словарь смежности вершин
    :param gateway: Шлюз
    :param node: Нода узла
    :return: None
    """
    if node in edges.get(gateway, []):
        edges[gateway].remove(node)
    if gateway in edges.get(node, []):
        edges[node].remove(gateway)


def rebuild_edges(edges: Dict[str, Set[str]], gateway: str, node: str) -> None:
    """
        Idea:
            Достраивание коридоров после проверки на закрытие шлюза
    :param edges: Словарь смежности вершин
    :param gateway: Шлюз
    :param node: Нода узла
    :return: None
    """
    edges[gateway].add(node)
    edges[node].add(gateway)


def main():
    edges = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.setdefault(node1, set()).add(node2)
                edges.setdefault(node2, set()).add(node1)

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
