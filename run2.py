import sys
from collections import deque
from typing import List, Dict, Tuple, Set


def find_shortest_path(edges: Dict[str, Set[str]], start: str) -> int | float:
    """
        Idea:
            Поиск минимальной длины пути до шлюза
    :param edges: Словарь смежности вершин
    :param start: Стартовая точка
    :return: depth длина пути
    """
    q = deque([(start, 0)])
    visited = {start}
    while q:
        node, depth = q.popleft()
        if node.isupper():
            return depth
        for neighbor in edges[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append((neighbor, depth + 1))
    return float('inf')


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


def find_edge_to_break(edges: Dict[str, Set[str]], start: str) \
        -> Tuple[str, str]:
    """
        Idea:
            Поиск лексикографически меньшего шлюза для разрыва,
            чтобы у нас оставалась возможность закрыть вирус внутри
    :param edges: Словарь смежности вершин
    :param start: Стартовая точка
    :return: Пара (шлюз, нода откуда пришли в шлюз)
    """
    gateways = [n for n in edges if n.isupper()]
    current_distance = find_shortest_path(edges, start)
    candidates = []

    for g in sorted(gateways):
        for neighbor in sorted(edges[g]):
            break_halls(edges, g, neighbor)
            new_distance = find_shortest_path(edges, start)
            if new_distance >= current_distance:
                candidates.append((g, neighbor))
            rebuild_edges(edges, g, neighbor)
    if not candidates:
        return None
    candidates.sort()
    return candidates[0]


def solve(edges: Dict[str, Set[str]]) -> List[str]:
    """
        Idea:
            Симуляция движения вируса и удаления шлюзов.
            Как только убрали все опасные шлюзы - return
    :param edges: Словарь смежности вершин
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    result = []
    current_pos = 'a'

    while True:
        candidate = find_edge_to_break(edges, current_pos)
        if not candidate:
            break

        gateway, node = candidate
        result.append(f"{gateway}-{node}")
        break_halls(edges, gateway, node)

        next_pos = find_virus_next_step(edges, current_pos)
        if not next_pos:
            break
        current_pos = next_pos

    return result


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
