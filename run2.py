import sys
from collections import deque
from typing import List, Dict, Set, Optional


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


def do_isolation(edges: Dict[str, set], virus_pos: str) -> Optional[List[str]]:
    """
        Idea:
        Проверка на то, что мы можем закрыть шлюз и затем найти
        решение для полученного графа
    :param edges:
    :param virus_pos:
    :return: True если мы можем закрыть шлюз и затем найти решение
    для полученного графа
    """
    if is_virus_closed(edges, virus_pos):
        return []
    if virus_pos.isupper():
        return None

    gateways = sorted([node for node in edges if node.isupper()])
    for gateway in gateways:
        for neigh in sorted(edges[gateway]):
            break_edges(edges, gateway, neigh)
            next_pos = find_virus_next_step(edges, virus_pos)
            if not next_pos:
                rebuild_edges(edges, gateway, neigh)
                return [f'{gateway}-{neigh}']
            deeper_solution = do_isolation(edges, next_pos)
            rebuild_edges(edges, gateway, neigh)
            if deeper_solution is not None:
                return [f'{gateway}-{neigh}'] + deeper_solution
    return None


def find_virus_next_step(edges: Dict[str, Set[str]], start: str) \
        -> Optional[str]:
    """
        Idea:
        Поиск следующего хода вируса.
        бфс до ближайшего меньшего по лексике шлюза с наименьшим путем
    :param edges: Словарь смежности вершин
    :param start: Стартовая точка
    :return: result_first_step - Первый шаг бфс для найденного шлюза
    """
    q = deque([(node, node, 1) for node in sorted(edges[start])])
    visited = {start}
    candidates = []

    while q:
        first_step, current_node, depth = q.popleft()
        if current_node.isupper():
            candidates.append((current_node, first_step, depth))
            continue
        for neigh in sorted(edges[current_node]):
            if neigh not in visited:
                visited.add(neigh)
                q.append((first_step, neigh, depth + 1))

    if not candidates:
        return None
    min_depth = min(candidates, key=lambda x: x[2])[2]
    best_candidates = [c for c in candidates if c[2] == min_depth]
    best_candidates.sort(
        key=lambda x: (x[0], x[1]))
    return best_candidates[0][1]


def solve(edges: Dict[str, Set[str]]) -> List[str]:
    """
        Idea:
        Рекурсивный спуск с перебором вариантов закрытия шлюзов
    :param edges: Словарь смежности вершин
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    return do_isolation(edges, 'a')


def break_edges(edges: Dict[str, Set[str]], gateway: str, node: str) -> None:
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
